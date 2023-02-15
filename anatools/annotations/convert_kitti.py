import os
import json
import yaml
import numpy as np
from PIL import Image


def get_image_size(metadata, imagesdir):
    """ Helper function to get properties of an image"""
    if 'sensor' in metadata and 'resolution' in metadata['sensor']:
        imagesize = metadata['sensor']['resolution']
    else:
        image = Image.open(os.path.join(imagesdir, metadata['filename']))
        imagesize = image.size
    return imagesize


def kitti_label(cat, objann, image_size, metadata):
    """ Create a KITTI label for an object.
    # Support perspective / rectilinear projections as well as orthographic projections

    Kitti label format:
    - https://docs.nvidia.com/metropolis/TLT/archive/tlt-20/tlt-user-guide/text/preparing_data_input.html
    - https://github.com/bostondiditeam/kitti/blob/master/resources/devkit_object/readme.txt
    """
    # Commonly used inputs
    sensor_metadata = metadata['sensor']
    lens_type = 'perspective' # default lens type to perspective
    if 'lens_type' in sensor_metadata: lens_type = sensor_metadata['lens_type']

    # Build the label array
    label = list()

    # Category name: str (1 entry)
    label.append(cat.lower().replace(' ', ''))  # NVIDIA models require lowercase names

    # Is truncated: float for leaving image boundary (1 entry) 
    truncated = '0.0'
    if objann.get('truncated', False): truncated = '1.0'
    label.append(truncated)

    # Occluded level: int (fully visible, largely visible, largely occluded, unk): int in the set [0,1,2,3] (1 entry)
    occlusionLevel = '3'
    if objann.get('obstruction', None)!=None:
        if objann['obstruction'] == 0.0:    occlusionLevel = '0'
        elif objann['obstruction'] < 0.5:   occlusionLevel = '1'
        else:                               occlusionLevel = '2'
    label.append(occlusionLevel)

    # Observation angle: float [-pi..pi] (1 entry)
    centroid = np.array([objann['centroid'][1], objann['centroid'][0]])
    imageCenter = np.array(image_size) / 2

    if lens_type == 'perspective' and 'camera_size' in sensor_metadata and 'focal_length' in sensor_metadata:
        # https://en.wikipedia.org/wiki/Angle_of_view
        angle_of_view = 2 * np.arctan(sensor_metadata['camera_size'] / (2 * sensor_metadata['focal_length']))
        # hfov = 2*sensor_metadata['target_distance']*np.tan(angle_of_view/2)
        # px_per_distance = image_size[0]/hfov  # pixels per mm

        r_px = np.linalg.norm(centroid - imageCenter)
        alpha = r_px / image_size[0] * angle_of_view  #linear model of full angle

    elif 'gsd_at_nadir' in sensor_metadata:
        distance_from_sensor = objann['distance']  # TODO check lens_orthographic_scale

        if sensor_metadata['look_angle']:
            raise # TODO: assuming sensor is in center of image pointing straight down
        if sensor_metadata['azimuth'] != 180:
            raise # TODO: assuming pixel grid is aligned with the camera reference frame

        distance_from_center = np.linalg.norm(centroid-imageCenter)*sensor_metadata['gsd_at_nadir']
        alpha = np.arccos(distance_from_center/distance_from_sensor)
    else:
        alpha = 0

    label.append(str(alpha))

    # bbox coords [xmin, ymin, xmax, ymax]: integers (4 entries)
    xmin = objann['bbox'][0]
    ymin = objann['bbox'][1]
    xmax = xmin + objann['bbox'][2]
    ymax = ymin + objann['bbox'][3]
    label.extend([str(xmin), str(ymin), str(xmax), str(ymax)])

    # 3-D dimension of the object (in real distance units): floats (3 entries)
    length, width, height = objann.get('size', [1.0, 1.0, 1.0])
    label.extend([str(height), str(width), str(length)])

    # 3-D object location x, y, z in camera coordinates (in real distance units): floats (3 entries)
    if lens_type == 'perspective':
        distance_from_sensor = objann['distance']
        r = distance_from_sensor * np.sin(alpha)
        z = distance_from_sensor * np.cos(alpha)

        deltax_px = centroid[0] - imageCenter[0]
        deltay_px = centroid[1] - imageCenter[1]
        if deltax_px == 0:
            x = 0
            y = r
        else:
            theta = np.arctan(deltay_px/deltax_px)
            x = r * np.sin(theta)
            y = r * np.cos(theta)

    elif 'gsd_at_nadir' in sensor_metadata:  # Orthographic Projection
        x = (centroid[0]-imageCenter[0])*sensor_metadata['gsd_at_nadir']
        y = (centroid[1]-imageCenter[1])*sensor_metadata['gsd_at_nadir']
        #z = objann['distance'] * #TODO check lens_orthographic_scale
        z = 36000000.0
    else:
        x,y,z = 0,0,0

    label.extend([str(x), str(y), str(z)])

    # Rotation ry about the Y-axis in camera coordinates: float [-pi..pi] (1 entry)
    # In Euler angles this would be the 'yaw' as y-axiz in camera coords is z-axis in Euler math (and in Blender)
    rotation = objann.get('rotation', [0.0, 0.0, 0.0])
    label.append(str(rotation[2]))

    return ' '.join(label)


def convert_kitti(datadir, outdir, mapping):
    """ To use the data in KITTI format. Result will be placed in outdir
    """
    # Input directories
    imagesdir = os.path.join(datadir, 'images')
    annsdir = os.path.join(datadir, 'annotations')
    metadir = os.path.join(datadir, 'metadata')


    # for each interpretation, gather annotations and map categories
    for annsfilename in os.listdir(annsdir):
        with open(os.path.join(annsdir, annsfilename), 'r') as af:
            anns = json.load(af)
        with open(os.path.join(metadir, annsfilename.replace('ana', 'metadata')), 'r') as mf:
            metadata = json.load(mf)

        imageSize = get_image_size(metadata, imagesdir)

        filename = anns['filename'].split('.')[0]
        labelfile = open('{}/{}.txt'.format(outdir, filename), 'w+')
        # for each object in the metadata file, check if any of the properties are true
        for obj in metadata['objects']:
            for prop in mapping['properties']:
                if eval(prop):
                    for ann in anns['annotations']:
                        if ann['id'] == obj['id']:
                            objann = ann
                            break
                    else:  # All the objects from the scene are recorded in metadata; only those in the image are annotated
                        continue

                    cat = mapping['classes'][mapping['properties'][prop]]

                    # Metadata needed to make Kitti labels from annotations:
                    if 'channel' in metadata and metadata['channel'] == 'satrgb':
                        metadata['sensor'].update({
                            'lens_type': 'orthographic',
                            'lens_orthographic_scale': 1.0
                        })
                    if 'sensor' not in metadata:
                        metadata['sensor'] = {
                            'lens_type': 'perspective',
                            'focal_length': 50,
                            'camera_size': 36  # width
                        }

                    label = kitti_label(cat[-1], objann, imageSize, metadata)
                    labelfile.write(label + '\n')

                    break

        labelfile.close()