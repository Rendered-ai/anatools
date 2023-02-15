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
from dataclasses import dataclass, field
import os
import sys
import logging
import copy
from anatools.lib.generator import ObjectGenerator
import bpy

logger = logging.getLogger(__name__)

@dataclass
class FileObject:
    """ A file stored on a volume """
    filename: str
    metadata: dict = field(default_factory=dict)

def blender_load(self, **kwargs):
    """
    Load a blender file. Doesn't require a collection name.
    """

    if self.loaded:
        # only load the object once
        return

    blender_file = kwargs.pop("blender_file")
    # load the objects
    with bpy.data.libraries.load(filepath="//" + blender_file, link=False) as (df, dt):
        dt.objects = df.objects
    
    name = dt.objects[0].name
    self.collection = bpy.data.collections.new(name)
    bpy.data.collections[name].objects.link(dt.objects[0])
    
    bpy.context.scene.collection.children.link(self.collection)

    self.root = dt.objects[0]
    self.loaded = True
    self.object_type = name

    # save object config if it was provided
    if "config" in kwargs:
        self.config = kwargs.pop("config")

def file_to_objgen(generators, object_class):
    """
    Process a mixed list of generators and FileObjects.
    For any FileObject in the list, wrap it in an ObjectGenerator. The object type returned by the
    generator will be 'object_class'. The loader method will be replaced with one appropriate
    to the file type specified in the FileObject (currently only Blender is supported)
    """

    # return generators
    wrapped_generators = []
    for generator in generators:
        if isinstance(generator, FileObject):
            # it's a file object - copy the class so we can change the load method
            new_generator_class = type('DynamicObject', object_class.__bases__, dict(object_class.__dict__))
            _, ext = os.path.splitext(generator.filename)
            if ext == ".blend":
                new_generator_class.load = blender_load
            else:
                logger.error(f"File type of '{ext}' not supported")
                sys.exit(1)
            wrapped_generator = ObjectGenerator(
                new_generator_class,
                None,
                blender_file=generator.filename)
        else:
            # it's already a generator
            wrapped_generator = generator
        wrapped_generators.append(wrapped_generator)

    return wrapped_generators