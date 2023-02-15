# Copyright 2019-2022 DADoES, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the root directory in the "LICENSE" file or at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import json
import logging
import datetime
import bpy
import cv2
import numpy
import anatools.lib.context as ctx

logger = logging.getLogger(__name__)
loglevel = logging.getLogger().level

# pylint: disable=method-hidden
# pylint: disable=W0221

class MetadataEncoder(json.JSONEncoder):
    """ Custom encoder to convert metadata to JSON """
    def default(self, obj):
        if hasattr(obj, 'dump_metadata'):
            return obj.dump_metadata()
        return json.JSONEncoder.default(self, obj)


class AnaScene:
    """ Base class for a scene """
    def __init__(self, blender_scene=None, annotation_view_layer=None, objects=None, sensor_name="Image"):
        """ initialize scene """
        self.filename = None # this is set when annotations are written
        self.sensor_name = sensor_name
        self.blender_scene = blender_scene
        if annotation_view_layer is None:
            self.annotation_view_layer = bpy.context.view_layer
        else:
            self.annotation_view_layer = annotation_view_layer
        self.configure_compositor()

        self.objects = []
        if objects is not None:
            for obj in objects:
                self.add_object(obj)

    def dump_metadata(self):
        """ Dump metadata """
        # only show metadata for objects that were rendered
        rendered_objects = []
        for obj in self.objects:
            if obj.rendered:
                rendered_objects.append(obj)
        return {
            "filename": self.filename,
            "channel": ctx.channel.name,
            "version": '0.0.1',
            "date": datetime.datetime.now().isoformat(),
            "objects": rendered_objects}
   
    def configure_compositor(self):
        """ configure the compositor """
        self.blender_scene.use_nodes = True
        self.annotation_view_layer.use_pass_object_index = True
        nodes = self.blender_scene.node_tree.nodes
        links = self.blender_scene.node_tree.links
        filename = f'{ctx.interp_num:010}-#-{self.sensor_name}'

        self.imgout = nodes.new('CompositorNodeOutputFile') #output image node
        self.imgout.name = 'imgout'
        self.imgout.base_path = os.path.join(ctx.output, "images")
        self.imgout.format.file_format = "PNG"
        self.imgout.format.color_depth = "8"
        self.imgout.format.compression = 0
        self.imgout.file_slots.clear()
        self.imgout.file_slots.new(filename)

        self.maskout = nodes.new('CompositorNodeOutputFile') #output mask node
        self.maskout.name = 'maskout'
        self.maskout.base_path = os.path.join(ctx.output, "masks")
        self.maskout.format.file_format = "PNG"
        self.maskout.format.color_mode = "BW"
        self.maskout.format.color_depth = "16"
        self.maskout.format.compression = 0
        self.maskout.file_slots.remove(self.maskout.inputs['Image'])
        self.maskout.file_slots.new(filename)
        self.maskoutput = None
        self.mask = os.path.join(ctx.output, 'masks', filename)

        self.last_output = nodes['Render Layers'].outputs['Image']
        self.last_link = links.new(self.last_output, self.imgout.inputs[0])

    def add_object(self, obj, ooi=True):
        """ add an object to the scene """
        self.objects.append(obj)
        self.configure_mask(obj)
        obj.rendered = True
        obj.ooi = ooi  #Default is that the objects added to the Anascene are objects of interest.
        obj.active_scene = self.blender_scene

    def configure_mask(self, obj):
        """ set the pass index for the object and each of its subobjects """
        if not self.blender_scene.use_nodes:
            logger.info("AnaScene.configure_mask: Something's wrong!")
            self.configure_compositor()

        nodes = self.blender_scene.node_tree.nodes
        links = self.blender_scene.node_tree.links

        obj.root.pass_index = obj.instance
        children = [child.name for child in obj.root.children]
        while len(children):
            bpy.data.objects[children[0]].pass_index = obj.instance
            for child in bpy.data.objects[children[0]].children:
                children.append(child.name)
            children.pop(0)

        # maskroot = f'{ctx.interp_num:010}-{obj.root.name}-#'
        # self.maskout.file_slots.new(maskroot)

        logger.debug(f"Adding IDMask Node for {obj.root.name}")
        masknode = nodes.new('CompositorNodeIDMask')
        masknode.name = obj.root.name + '_mask'
        masknode.index = obj.instance
        links.new(nodes['Render Layers'].outputs['IndexOB'], masknode.inputs['ID value'])
        dividenode = nodes.new('CompositorNodeMath')
        dividenode.name = obj.root.name +'_divide'
        dividenode.operation = 'DIVIDE'
        dividenode.inputs[1].default_value = 65535/obj.instance
        links.new(masknode.outputs['Alpha'], dividenode.inputs[0])
        if self.maskoutput is None:
            self.maskoutput = dividenode.outputs[0]
            links.new(dividenode.outputs[0], self.maskout.inputs[0])
        else:
            links.remove(self.maskout.inputs[0].links[0])
            maxnode = nodes.new('CompositorNodeMath')
            maxnode.name = obj.root.name + '_max'
            maxnode.operation = 'MAXIMUM'
            links.new(self.maskoutput, maxnode.inputs[0])
            links.new(dividenode.outputs[0], maxnode.inputs[1])
            links.new(maxnode.outputs[0], self.maskout.inputs[0])
            self.maskoutput = maxnode.outputs[0]

        if not os.path.isdir(os.path.join(ctx.output, 'masks')):
            os.mkdir(os.path.join(ctx.output, 'masks'))


    def write_ana_annotations(self, calculate_obstruction=False):
        """ Creates an annotations file of the image in <output>/annotations/{imgfile}-anatools.json """
        if not self.filename: self.filename = f'{ctx.interp_num:010}-{self.blender_scene.frame_current}-{self.sensor_name}.png'
        if not os.path.isdir(os.path.join(ctx.output, 'annotations')):
            os.mkdir(os.path.join(ctx.output, 'annotations'))
        annfile = os.path.join(ctx.output, 'annotations', f'{ctx.interp_num:010}-{self.blender_scene.frame_current}-{self.sensor_name}-ana.json')

        logger.info(f"Writing annotations to: {annfile}")

        # generate list of annotations
        ann_list = []
        for obj in self.objects:
            if obj.rendered and obj.ooi:
                logger.debug(f"Generated annotation for {obj.root.name}")
                obj.mask = os.path.join(ctx.output, f'masks/{ctx.interp_num:010}-#-{self.sensor_name}.png')
                ann = obj.dump_annotations(calculate_obstruction=calculate_obstruction)
                if ann: ann_list.append(ann)

        annotation_out = {
            "filename": self.filename,
            "annotations": ann_list
        }

        with open(annfile, 'w') as f:
            json.dump(annotation_out, f, indent=4)


    def write_ana_metadata(self):
        """ Creates a metadata file of the image in <output>/metadata/{filename}-meta.json """
        if not os.path.isdir(os.path.join(ctx.output, 'metadata')):
            os.mkdir(os.path.join(ctx.output, 'metadata'))
        metafile = os.path.join(ctx.output, 'metadata', f'{ctx.interp_num:010}-{self.blender_scene.frame_current}-{self.sensor_name}-metadata.json')

        logger.info(f"Writing metadata to: {metafile}")

        with open(metafile, "w") as f:
            json.dump(self, f, cls=MetadataEncoder, indent=4)
