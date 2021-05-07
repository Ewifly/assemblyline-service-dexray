import os, string, tempfile, glob
from pathlib import Path
from os import listdir
from os.path import isfile, join

from assemblyline.common.str_utils import safe_str
from assemblyline_v4_service.common.base import ServiceBase
from assemblyline_v4_service.common.result import Result, ResultSection, BODY_FORMAT
from yaml import add_constructor

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
        text_section.add_line("aftr cmd")
        if my_cmd_output:
            text_section.add_line("command success")
            self.log.info(f"command success")
            cwd = self.working_directory
            filename = request.file_name
            self.log.info(f"workingdir = {cwd}")
            text_section.add_line("workingdir = ", cwd)
            self.log.info(f"filename = {filename}")
            text_section.add_line("file name = ", filename)

            lnewfile_path = glob.glob(cwd + filename + ".*")
            self.log.info(f"newfile path = {lnewfile_path}")
            if lnewfile_path:
                text_section.add_line("in cwd")
                text_section.add_line()
                newfile_path = lnewfile_path[0]
                newfile_name = os.path.basename(newfile_path)
                self.log.info(f"newfile_name = {newfile_name}")
                request.add_extracted(cwd, newfile_name, "resubmit")
                text_section.add_line(f"file resubmitted as: {newfile_name}")
                self.log.info(f"file resubmitted")
            path = request.file_path
            self.log.info(f"path = {path}")
            lnewfile_path = glob.glob(path + ".*")
            self.log.info(f"newfile path = {lnewfile_path}")
            if lnewfile_path:
                text_section.add_line("in filepath")
                newfile_path = lnewfile_path[0]
                newfile_name = os.path.basename(newfile_path)
                self.log.info(f"newfile_name = {newfile_name}")
                request.add_extracted(path, newfile_name, "resubmit")
                text_section.add_line(f"file resubmitted as: {newfile_name}")
                self.log.info(f"file resubmitted")

        request.result = result
        