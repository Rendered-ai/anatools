from anatools.annotations.convert_sagemaker import convert_sagemaker_od
from .convert_coco import convert_coco
from .convert_kitti import convert_kitti
from .convert_pascal import convert_pascal
from .convert_sagemaker import convert_sagemaker_od, convert_sagemaker_ss
from .convert_yolo import convert_yolo
from .draw import draw
import yaml

class annotations:
    """Generates annotations given a dataset directory, an output directory and mapping file.
    The dataset directory must include the Ana annotations, images and metadata folders.
    Examples of mapfiles are in the example channel at /ana/channels/example/mapfiles/.
    """

    def bounding_box_2d(self, image_path, out_dir, object_ids=None, object_types=None, line_thickness=1):
        """
        Generates images annotated with 2d bounding boxes for datasets downloaded from the Platform. Optional filter on 
        object_ids or object_types (must choose a single filter).
        
        Parameters
        ----------
        image_path : str
            Path to of specific image file to draw the boxes for.  
        out_dir : str
            File path to directory where the image should be saved to.
        object_ids : list[int]
            List of object id's to annotate. If not provided, all objects will get annotated. Choose either id or type filter.
        object_types: list[str]
            Filter for the object types to annotate. If not provided, all object types will get annotated. Choose either id or type filter.
        line_thickness: int
            Desired line thickness for box outline. 
        """
        draw(image_path, out_dir, draw_type='box_2d', object_ids=object_ids, object_types=object_types, line_thickness=line_thickness)


    def bounding_box_3d(self, image_path, out_dir, object_ids=None, object_types=None, line_thickness=1):
        """
        Generates images annotated with 3d bounding boxes for datasets downloaded from the Platform. Optional filter on 
        object_ids or object_types (must choose a single filter).
        
        Parameters
        ----------
        image_path : str
            Path to of specific image file to draw the boxes for.  
        out_dir : str
            File path to directory where the image should be saved to.
        object_ids : list[int]
            List of object id's to annotate. If not provided, all objects will get annotated. Choose either id or type filter.
        object_types: list[str]
            Filter for the object types to annotate. If not provided, all object types will get annotated. Choose either id or type filter.
        line_thickness: int
            Desired line thickness for box outline. 
        """
        draw(image_path, out_dir, draw_type='box_3d', object_ids=object_ids, object_types=object_types, line_thickness=line_thickness)


    def segmentation(self, image_path, out_dir, object_ids=None, object_types=None, line_thickness=1):
        """
        Generates images annotated with outlines around objects for datasets downloaded from the Platform. Optional filter on 
        object_ids or object_types (must choose a single filter).
        
        Parameters
        ----------
        image_path : str
            Path to of specific image file to draw the boxes for.  
        out_dir : str
            File path to directory where the image should be saved to.
        object_ids : list[int]
            List of object id's to annotate. If not provided, all objects will get annotated. Choose either id or type filter.
        object_types: list[str]
            Filter for the object types to annotate. If not provided, all object types will get annotated. Choose either id or type filter.
        line_thickness: int
            Desired line thickness for object segmentation outline. 
        """
        draw(image_path, out_dir, draw_type='segmentation', object_ids=object_ids, object_types=object_types, line_thickness=line_thickness)


    def dump_coco(self, datadir, outdir, mapfile):
        """Generates annotations in the format of COCO Object Detection. See https://cocodataset.org/#format-data.
        
        Parameters
        ----------
        datadir : str
            The location of the Ana dataset.
        outdir : str
            The location to output the annotation files to.
        mapfile: str
            The location of the mapping file.
        """
        with open(mapfile) as f:
            mapping = yaml.safe_load(f)
        convert_coco(datadir, outdir, mapping)


    def dump_kitti(self, datadir, outdir, mapfile):
        """Generates annotations in the format of KITTI. See https://docs.nvidia.com/metropolis/TLT/archive/tlt-20/tlt-user-guide/text/preparing_data_input.html.
        
        Parameters
        ----------
        datadir : str
            The location of the Ana dataset.
        outdir : str
            The location to output the annotation files to.
        mapfile: str
            The location of the mapping file.
        """
        with open(mapfile) as f:
            mapping = yaml.safe_load(f)
        convert_kitti(datadir, outdir, mapping)


    def dump_pascal(self, datadir, outdir, mapfile):
        """Generates annotations in the format of PASCAL VOC. See https://pjreddie.com/media/files/VOC2012_doc.pdf.
        
        Parameters
        ----------
        datadir : str
            The location of the Ana dataset.
        outdir : str
            The location to output the annotation files to.
        mapfile: str
            The location of the mapping file.
        """
        with open(mapfile) as f:
            mapping = yaml.safe_load(f)
        convert_pascal(datadir, outdir, mapping)


    def dump_sagemaker_od(self, datadir, outdir, mapfile):
        """Generates annotations in the format of Sagemaker Object Detection. See https://docs.aws.amazon.com/sagemaker/latest/dg/object-detection.html.
        
        Parameters
        ----------
        datadir : str
            The location of the Ana dataset.
        outdir : str
            The location to output the annotation files to.
        mapfile: str
            The location of the mapping file.
        """
        with open(mapfile) as f:
            mapping = yaml.safe_load(f)
        convert_sagemaker_od(datadir, outdir, mapping)


    def dump_sagemaker_ss(self, datadir, outdir, mapfile):
        """Generates annotations in the format of Sagemaker Semantic Segmentation. See https://docs.aws.amazon.com/sagemaker/latest/dg/semantic-segmentation.html.
        
        Parameters
        ----------
        datadir : str
            The location of the Ana dataset.
        outdir : str
            The location to output the annotation files to.
        mapfile: str
            The location of the mapping file.
        """
        with open(mapfile) as f:
            mapping = yaml.safe_load(f)
        convert_sagemaker_ss(datadir, outdir, mapping)

    def dump_yolo(self, datadir, outdir, mapfile):
        """Generates annotations in the format of YOLO Object Detection.
        
        Parameters
        ----------
        datadir : str
            The location of the Ana dataset.
        outdir : str
            The location to output the annotation files to.
        mapfile: str
            The location of the mapping file.
        """
        with open(mapfile) as f:
            mapping = yaml.safe_load(f)
        convert_yolo(datadir, outdir, mapping)