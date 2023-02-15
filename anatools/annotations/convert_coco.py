import json
import yaml
import os
import datetime
from PIL import Image

def create_cocodata():
    cocodata = dict()
    cocodata['info'] = {    
        "description":  "Rendered.AI Synthetic Dataset",
        "url":          "https://rendered.ai/",
        "contributor":  "info@rendered.ai",
        "version":      "1.0",
        "year":         str(datetime.datetime.now().year),
        "date_created": datetime.datetime.now().isoformat()}
    cocodata['licenses'] = [{
        "id":   0,
        "url":  "https://rendered.ai/",     # "url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
        "name": "Rendered.AI License"}]     # "name": "Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License"}]
    cocodata['images'] = list()
    cocodata['categories'] = list()
    cocodata['annotations'] = list()
    return cocodata


def convert_coco(datadir, outdir, mapping):

    annsdir = os.path.join(datadir, "annotations")
    metadir = os.path.join(datadir, "metadata")
    imgdir = os.path.join(datadir, "images")
    annsfiles = os.listdir(annsdir)
    
    cocodata = create_cocodata()
    annotations = []
    categories = []
    cats = []
    imgid = 0
    annid = 0
        
     # for each interpretation, gather annotations and map categories
    for f in sorted(annsfiles):
        if not f.endswith('.json'):
            continue
        with open(os.path.join(annsdir,f), 'r') as af: anns = json.load(af)
        with open(os.path.join(metadir,f.replace('ana','metadata')), 'r') as mf: metadata = json.load(mf)
        
        # for each object in the metadata file, check if any of the properties are true
        for obj in metadata['objects']:
            for prop in mapping['properties']:
                if eval(prop):
                    for ann in anns['annotations']:
                        if ann['id'] == obj['id']: 
                            cat = mapping['classes'][mapping['properties'][prop]]
                            if cat not in cats: cats.append(cat)
                            annotation = {}
                            annotation['id'] = annid
                            annotation['image_id'] = imgid
                            annotation['category_id'] = cats.index(cat)
                            annotation['segmentation'] = ann['segmentation']
                            annotation['area'] = ann['bbox'][2] * ann['bbox'][3]
                            annotation['bbox'] = ann['bbox']
                            annotation['iscrowd'] = 0
                            annid += 1
                            cocodata['annotations'].append(annotation)
                            break
        imgdata = {
            'id':               imgid, 
            'file_name':        metadata['filename'], 
            'date_captured':    metadata['date'], 
            'license':          0 }
        if 'sensor' in metadata:
            metadata['width'] =  metadata['sensor']['resolution'][0],
            metadata['height']=  metadata['sensor']['resolution'][1],
            if 'frame' in metadata['sensor']: metadata['frame'] = metadata['sensor']['frame']
        else:
            im = Image.open(os.path.join(imgdir, anns['filename']))
            width, height = im.size
            metadata['width'] =  width
            metadata['height']=  height
        cocodata['images'].append(imgdata)
        imgid += 1
    for cat in cats:
        cocodata['categories'].append({
            'id':               cats.index(cat), 
            'name':             cat[-1],
            'supercategory':    cat[0]
        })

    with open(os.path.join(outdir,'coco.json'), 'w+') as of:
        json.dump(cocodata,of)
