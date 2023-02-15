import numpy as np
from PIL import Image, ImageDraw
import json
import os


def draw(image_path, out_dir, draw_type='box_2d', object_ids=None, object_types=None, line_thickness=1): 
    """
    This function handles the io and draws the right type of annotation on the image.

    Parameters
    ----------
    image_path : str
        Path to of specific image file to draw the boxes for.  
    out_dir : str
        File path to directory where the image should be saved to.
    draw_type : str
        Draw either a 2d bounding box, 3d bounding box, or segmentation on objects within an image. Must pass in either 'box_2d', 'box_3d', or 'segmentation' for values.
    object_ids : list[int]
        List of object id's to annotate. If not provided, all objects will get annotated. Choose either id or type filter.
    object_types: list[str]
        Filter for the object types to annotate. If not provided, all object types will get annotated. Choose either id or type filter.
    line_thickness: int
        Desired line thickness for box outline. 
    """

    if not os.path.exists(image_path):
        print('Incorrect path to images: ' + image_path)
        return

    if object_types and object_ids:
        print('Provide either object_types OR object_ids. ')
        return

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    root_dir = ('/').join(image_path.split('/')[:-2])
    image_name = image_path.split('/')[-1].split('.')[0]
    image_ext = image_path.split('/')[-1].split('.')[1]

    annotation_file = root_dir+'/annotations/'+image_name+"-ana.json"
    file = open(annotation_file)
    annotations = json.load(file)
    file.close()
    
    annotation_ids = [data['id'] for data in annotations['annotations']]
    if object_ids is not None and not check_lists(annotation_ids, object_ids, 'object_ids'):
        return
    
    
    metadata_file = root_dir+'/metadata/'+image_name+'-metadata.json'
    file = open(metadata_file)
    metadata = json.load(file)
    file.close()                    

    metadata_types = list(set([data['type'] for data in metadata['objects']]))
    
    # get object id and type to correspond to a unique color per type
    if object_ids:
        object_data = [data for data in metadata['objects'] if data['id'] in object_ids]
    elif object_types is not None:
        if not check_lists(metadata_types, object_types, 'object_types'):
            return  
        object_data = [data for data in metadata['objects'] if data['type'] in object_types]
    else:
        object_data = [data for data in metadata['objects']]

    # generate a unique color for each object type
    type_colors = {}

    for type in metadata_types:
        generate_color = [int(val) for val in np.random.randint(0, 255, 3)]
        type_colors[type] = tuple(generate_color)

    draw_img = Image.open(image_path)
    for object in annotations['annotations']:
        if any(object['id'] == d['id'] for d in object_data):
            color_info = [data for data in object_data if object['id'] == data['id']]
            if draw_type == 'box_2d':
                draw_img = box_2d(object['bbox'], draw_img, line_thickness, type_colors[color_info[0]['type']])
            elif draw_type == 'box_3d' :
                draw_img = box_3d(object['bbox3d'], draw_img, line_thickness, type_colors[color_info[0]['type']])
            elif draw_type == 'segmentation':
                draw_img = segmentation(object['segmentation'], draw_img, line_thickness, type_colors[color_info[0]['type']])
            else:
                print('Provide either box_2d, box_3d, or segmentation')

    outimg = out_dir+'/'+image_name+'-annotated-'+draw_type+'.'+image_ext
    draw_img.save(outimg)
    print(f'Image saved to {outimg}')


def box_2d(coordinates, bbox_img, width, outline):
    """
    Draws 2d boxes around objects given a list of coordinates.

    Parameters
    ----------
    coordinates : list
        The list of coordinates.
    bbox_img : array
        Image in form of a numpy array.
    width: int
        Desired line thickness for box outline. 
    outline: list
        List of bgr color values for PIL color inputs.

    Returns
    -------
    array
        Image in form of a numpy array with 2d boxes around objects.
    """
    x,y,w,h = coordinates
    draw = ImageDraw.Draw(bbox_img)
    draw.rectangle(((x,y), (x+w, y+h)), None, outline, width)
    return bbox_img


def box_3d(coordinates, bbox_img, width, fill):
    """
    Draws 3d boxes around objects given a list of coordinates.

    Parameters
    ----------
    coordinates : list
        The list of coordinates.
    bbox_img : array
        Image in form of a numpy array.
    width: int
        Desired line thickness for box outline. 
    fill: list
        List of bgr color values for PIL color inputs.
    
    Returns
    -------
    array
        Image in form of a numpy array with 3d boxes around objects.
    """
    point_1 = (coordinates[0], coordinates[1])
    point_2 = (coordinates[3], coordinates[4])
    point_3 = (coordinates[6], coordinates[7])
    point_4 = (coordinates[9], coordinates[10])
    point_5 = (coordinates[12], coordinates[13])
    point_6 = (coordinates[15], coordinates[16])
    point_7 = (coordinates[18], coordinates[19])
    point_8 = (coordinates[21], coordinates[22])
    draw = ImageDraw.Draw(bbox_img)
    draw.line((point_1, point_2), fill, width)
    draw.line((point_1, point_5), fill, width)
    draw.line((point_5, point_6), fill, width)
    draw.line((point_2, point_6), fill, width)
    draw.line((point_3, point_4), fill, width)
    draw.line((point_3, point_7), fill, width)
    draw.line((point_7, point_8), fill, width)
    draw.line((point_4, point_8), fill, width)
    draw.line((point_3, point_2), fill, width)
    draw.line((point_7, point_6), fill, width)
    draw.line((point_4, point_1), fill, width)
    draw.line((point_8, point_5), fill, width)
    return bbox_img


def segmentation(coordinates, draw_img, width, color):
    """
    Draws an outline around objects given a list of coordinates.

    Parameters
    ----------
    coordinates : list
        The list of coordinates.
    draw_img : array
        Image in form of a numpy array.
    width: int
        Desired line thickness for box outline. 
    fill: list
        List of bgr color values for cv2 color inputs.

    Returns
    -------
    array
        Image in form of a numpy array with objects outlined.
    """
    draw = ImageDraw.Draw(draw_img)
    for poly in coordinates:
        draw.polygon(poly, fill=None, outline=color, width=width)
    return draw_img


def check_lists(actual, expected, name_to_check):
    """
    Helper function that checks if one list is in another for validation on draw inputs.

    Parameters
    ----------
    actual : list
        The list of actual values found in either annotation or metadata file.
    expected : list
        The expected list that is provided from the user.
    name_to_check: str
        Name of parameter to check (either object_id or object_type).

    Returns
    -------
    bool
        True if lists are matching, False otherwise.
    """
    
    if not set(expected).issubset(set(actual)):
        out_of_bounds_check= list(set(expected) - set(actual))
        print(f'Provided {name_to_check} list has the following out of bounds: {out_of_bounds_check}. Please rerun with valid list. \nHere are all the {name_to_check} that can get annotated: ')
        print(list(set(actual)))
        return False
    return True