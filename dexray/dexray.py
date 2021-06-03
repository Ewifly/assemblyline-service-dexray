import os
import glob
from subprocess import Popen

from assemblyline_v4_service.common.base import ServiceBase
from assemblyline_v4_service.common.result import Result, ResultSection


class Dexray(ServiceBase):
    def __init__(self, config=None):
        super(Dexray, self).__init__(config)
        self.dexraytool = self.config.get("dexray_tool_path", None)

    def start(self):
        if not os.path.exists(self.dexraytool):
            self.log.error(f"Could not find dexray perl script at: {self.dexraytool}")

    def execute(self, request):
        file = request.file_path
        result = Result()
        unquar = Popen(["perl", self.dexraytool, file])
        unquar.wait()

        lnewfile_path = glob.glob(file + ".*")  # should find the newly created file (filename.<offset>_<AV Name>.out)
        if lnewfile_path:
            text_section = ResultSection('DexRay found files:')
            for newfile_path in lnewfile_path:
                vendor = newfile_path.rsplit("_", 1)[1].split(".out")[0]
                offset = newfile_path.rsplit("_", 1)[0].rsplit(".", 1)[1]
                newfile_name = f"{request.file_name}.{offset}_{vendor}"
                request.add_extracted(newfile_path, newfile_name, f"{vendor} un-quarantined file")
                text_section.add_line(f"Resubmitted {vendor} un-quarantined file as : {newfile_name}")
            result.add_section(text_section)
        request.result = result