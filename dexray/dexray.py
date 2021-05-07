import os, string, tempfile, glob
from pathlib import Path
from os import listdir
from os.path import isfile, join

from assemblyline.common.str_utils import safe_str
from assemblyline_v4_service.common.base import ServiceBase
from assemblyline_v4_service.common.result import Result, ResultSection, BODY_FORMAT

class Dexray(ServiceBase):
    def __init__(self, config=None):
        super(Dexray, self).__init__(config)

    def start(self):
        self.log.info(f"start() from {self.service_attributes.name} service called")

    def execute(self, request):

        result = Result()
        text_section = ResultSection('DexRay logs :')

        my_cmd = "perl dexray/dexray.pl " + request.file_path
        my_cmd_output = os.popen(my_cmd)
        if my_cmd_output:
            for line in my_cmd_output:
                text_section.add_line(line.rstrip())
            result.add_section(text_section)
            self.log.info(f"command success")

            self.log.info(f"workingdir = {self.working_directory}")
            self.log.info(f"filename = {request.file_name}")
            cwd = self.working_directory

            lnewfile_path = glob.glob(cwd + request.file_name + ".*")
            self.log.info(f"newfile path = {lnewfile_path}")
            if lnewfile_path:
                newfile_path = lnewfile_path[0]
                newfile_name = newfile_path.split("/")[-1]
                self.log.info(f"newfile_name = {newfile_name}")
                request.add_extracted(cwd, newfile_name, "resubmit")
                self.log.info(f"file resubmitted")
            # path = request.file_path
            # self.log.info(f"path = {path}")
            # lnewfile_path = glob.glob(path + ".*")
            # self.log.info(f"newfile path = {lnewfile_path}")
            # if lnewfile_path:
            #     newfile_path = lnewfile_path[0]
            #     newfile_name = newfile_path.split("/")[-1]
            #     self.log.info(f"newfile_name = {newfile_name}")
            #     request.add_extracted(path, newfile_name, "resubmit")
            #     self.log.info(f"file resubmitted")

        request.result = result
        