import logging
import os
from anatools.lib.node import Node
import anatools.lib.context as ctx
from anatools.lib.file_handlers import FileObject

logger = logging.getLogger(__name__)

class VolumeFile(Node):
    """ Create a file object from a volume file """

    def exec(self):
        """Execute node"""

        file_desc = self.inputs["File"][0]
        volume_id, rel_path = file_desc.split(":/")
        filename = os.path.join(ctx.data, 'volumes', volume_id, rel_path)
        file_object = FileObject(filename)

        return {"File": file_object}
