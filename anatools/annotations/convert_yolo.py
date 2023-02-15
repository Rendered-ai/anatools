import json
import os
from PIL import Image

def convert(size, box):
    """
    Convert bounding box to yolo format:
    https://stackoverflow.com/questions/56115874/how-to-convert-bounding-box-x1-y1-x2-y2-to-yolo-style-x-y-w-h
    """
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_yolo(datadir, outdir, mapping):
    """ Generate annotations in YOLO format. Result will be placed in outdir.

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
        with open(os.path.join(annsdir,f), 'r') as af:
            anns = json.load(af)
        with open(os.path.join(metadir,f.replace('ana','metadata')), 'r') as mf:
            metadata = json.load(mf)
        
        try:
            image = Image.open(os.path.join(imagedir, anns['filename']))
            width = image.size[0]
            height = image.size[1]
        except:
            raise Exception(f'Could not find a supported image for {anns["filename"]} in the dataset images directory.')

        # for each object in the metadata file, check if any of the properties are true
        yolodata = ""
        for obj in metadata['objects']:
            for prop in mapping['properties']:
                if eval(prop):
                    for ann in anns['annotations']:
                        if ann['id'] == obj['id']:
                            objann = ann
                    size = (width, height)
                    xmin = objann['bbox'][0]
                    ymin = objann['bbox'][1]
                    xmax = objann['bbox'][0] + objann['bbox'][2]
                    ymax = objann['bbox'][1] + objann['bbox'][3]
                    box = (xmin, xmax, ymin, ymax)
                    x, y, w, h = convert(size, box)
                    cls = mapping['properties'][prop]
                    objectdata = f"{cls} {x} {y} {w} {h}\n"
                    yolodata += objectdata
                    break
        
        # write xmlfile
        with open(os.path.join(outdir,f.replace('-ana.json','.txt')), 'w+') as txtfile:
            txtfile.write(yolodata)