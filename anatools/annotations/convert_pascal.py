import json
import yaml
import os
from PIL import Image

def generate_xml(object, xml=None, level=0):
    if xml is None: xml = ''
    for key in object.keys():
        if (type(object[key]) is list):
            for val in object[key]:
                xml += '\t'*level+f'<object>\n'
                xml = generate_xml(val, xml, level+1)
                xml += '\t'*level+f'</object>\n'
        elif (type(object[key]) is dict): 
            xml += '\t'*level+f'<{key}>\n'
            xml = generate_xml(object[key], xml, level+1)
            xml += '\t'*level+f'</{key}>\n'
        else: xml += '\t'*level+f'<{key}>{object[key]}</{key}>\n'
    return xml


def convert_pascal(datadir, outdir, mapping):
    """ Generate annotations in PASCAL VOC format. Result will be placed in outdir.

    Parameters
    ----------
    datadir : str
        Location of Rendered.ai dataset output.
    outdir : str
        Location where the results should be written.
    mapfile: str
        The map file used for annotations (YAML only).
    
    Returns
    -------
    """
    annsdir = os.path.join(datadir, "annotations")
    metadir = os.path.join(datadir, "metadata")
    imagedir = os.path.join(datadir, "images")
    annsfiles = os.listdir(annsdir)

    # for each interpretation, gather annotations and map categories
    for f in sorted(annsfiles):
        with open(os.path.join(annsdir,f), 'r') as af: anns = json.load(af)
        with open(os.path.join(metadir,f.replace('ana','metadata')), 'r') as mf: metadata = json.load(mf)
        
        image = Image.open(os.path.join(imagedir,anns['filename']))
        width = image.size[0]
        height = image.size[1]
        depth = len(image.getbands())
        xmldata = {
            'annotation': {
                'folder': 'images',
                'filename': anns['filename'],
                'path': 'images/'+anns['filename'],
                'source': {'database': 'Unknown'},
                'size': {
                    'width': width,
                    'height': height,
                    'depth': depth
                },
                'segmented': 0,
                'objects': []
            }
        }

        # for each object in the metadata file, check if any of the properties are true
        for obj in metadata['objects']:
            for prop in mapping['properties']:
                if eval(prop):
                    for ann in anns['annotations']:
                        if ann['id'] == obj['id']: objann = ann
                    objectdata = {
                        'name': mapping['classes'][mapping['properties'][prop]][-1],
                        'pose': 'Unspecified',
                        'truncated': 0,
                        'difficult': 0,
                        'bndbox': {
                            'xmin': objann['bbox'][0],
                            'ymin': objann['bbox'][1],
                            'xmax': objann['bbox'][0] + objann['bbox'][2],
                            'ymax': objann['bbox'][1] + objann['bbox'][3]
                        }
                    }
                    xmldata['annotation']['objects'].append(objectdata)
                    break
        
        # write xmlfile
        text = generate_xml(xmldata)
        with open(os.path.join(outdir,f.replace('-ana.json','.xml')), 'w+') as xmlfile:
            xmlfile.write(text)