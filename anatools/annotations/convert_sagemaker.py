import os
import yaml
import json
from PIL import Image, ImageDraw

def convert_sagemaker_od(datadir, outdir, mapping):
    """ Generate annotations for AWS Sagemaker. Annotation jpegs will be placed in <datadir>/<outputdir>.
    
    Parameters
    ----------
    datadir : str
        Location of Rendered.ai dataset output.
    outputdir : str
        Name of directory where the results should be written.
    mapfile: str
        The map file used for annotations (YAML only).
    
    Returns
    -------

    """

    annsdir = os.path.join(datadir, "annotations")
    metadir = os.path.join(datadir, "metadata")

    # Get the image shape
    sample_image_filename = [datadir + '/images/' + imgfilename for imgfilename in os.listdir(datadir + '/images')][0]
    sample_image = Image.open(sample_image_filename)
    imgshape = [sample_image.size[0], sample_image.size[1], 3]

    sodcats = list()
    for annsfilename in os.listdir(annsdir):
        with open(os.path.join(annsdir, annsfilename), 'r') as af:
            anns = json.load(af)
        with open(os.path.join(metadir, annsfilename.replace('ana', 'metadata')), 'r') as mf:
            metadata = json.load(mf)

        soddata = dict()
        soddata['file'] = anns['filename'].split('.')[0] + '.jpeg'  # Sagemaker requires images be in jpeg format
        soddata['image_size'] = [{'width':imgshape[0],'height':imgshape[1],'depth':imgshape[2]}]
        soddata['annotations'] = list()
        for obj in metadata['objects']:
            for i, prop in enumerate(mapping['properties']):
                if eval(prop):
                    for ann in anns['annotations']:
                        if ann['id'] == obj['id']:
                            objann = ann
                            break
                    else:  # All the objects from the scene are recorded in metadata; only those in the image are annotated
                        continue

                    rai_cat_id = mapping['properties'][prop]
                    cat = mapping['classes'][rai_cat_id]
                    cat_name = cat[-1]
                    if cat_name not in sodcats: sodcats.append(cat_name)              
                    soddata['annotations'].append({
                        'class_id': sodcats.index(cat_name),
                        'left':     objann['bbox'][0],
                        'top':      objann['bbox'][1],
                        'width':    objann['bbox'][2],
                        'height':   objann['bbox'][3]
                    })
                    break

        soddata['categories'] = list()
        for cId, cName in enumerate(sodcats):
            soddata['categories'].append({'class_id':cId, 'name':cName})
    
        outfile = os.path.join(outdir, '{}.json'.format(anns['filename'].split('.')[0]))
        with open(outfile, 'w') as f:
            json.dump(soddata, f)


def convert_sagemaker_ss(datadir, outdir, mapping):
    """ Generate masks for AWS Sagemaker Semantic Segmentation. Mask pngs will be placed in <datadir>/<outputdir>.
    
    Parameters
    ----------
    datadir : str
        Location of Rendered.ai dataset output.
    outputdir : str
        Name of directory where the results should be written.
    mapfile: str
        The map file used for annotations (YAML only).
    
    Returns
    -------
    """

    annsdir = os.path.join(datadir, "annotations")
    metadir = os.path.join(datadir, "metadata")

    # Get the image shape
    sample_image_filename = [datadir + '/images/' + imgfilename for imgfilename in os.listdir(datadir + '/images')][0]
    sample_image = Image.open(sample_image_filename)
    imgshape = [sample_image.size[0], sample_image.size[1], 3]

    for annsfilename in os.listdir(annsdir):
        with open(os.path.join(annsdir, annsfilename), 'r') as af:
            anns = json.load(af)
        with open(os.path.join(metadir, annsfilename.replace('ana', 'metadata')), 'r') as mf:
            metadata = json.load(mf)
        maskimg = Image.new("L", (imgshape[0], imgshape[1]))
        draw = ImageDraw.Draw(maskimg)

        for obj in metadata['objects']:
            for prop in mapping['properties']:
                if eval(prop):
                    for ann in anns['annotations']:
                        if ann['id'] == obj['id']:
                            objann = ann
                            break
                    rai_cat_id = mapping['properties'][prop]
                    draw.polygon(objann['segmentation'][0], fill=rai_cat_id, outline=rai_cat_id)
                    break

        maskimg.save(os.path.join(outdir, f'{anns["filename"].split(".")[0]}.png'))