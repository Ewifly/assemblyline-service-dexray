import os, string, tempfile, glob, sys
from pathlib import Path
from os import listdir
from os.path import isfile, join
from subprocess import Popen, PIPE, call

from assemblyline.common.str_utils import safe_str
from assemblyline_v4_service.common.base import ServiceBase
from assemblyline_v4_service.common.result import Result, ResultSection, BODY_FORMAT
from yaml import add_constructor

class Dexray(ServiceBase):
    def __init__(self, config=None):
        super(Dexray, self).__init__(config)
        self.dexraytool = self.config.get("dexray_tool_path", None)
    def start(self):
        self.log.info(f"start() from {self.service_attributes.name} service called")

    def execute(self, request):
        self.log.info(f"tool path = {self.dexraytool}")
        file = request.file_path
        cwd = self.working_directory
        filename = request.file_name
        self.log.info(f"file = {file}")
        result = Result()
        text_section = ResultSection('DexRay logs :')
        # my_cmd = "perl" + os.getcwd() + "dexray/dexray.pl " + request.file_path

        print(os.getcwd())
        unquar = Popen(["perl", self.dexraytool, file])
        unquar.wait()
        self.log.info(f"command success")

        self.log.info(f"workingdir = {cwd}")
        self.log.info(f"filename = {filename}")

        path = request.file_path
        lnewfile_path = glob.glob(path + ".*")
        self.log.info(f"newfile path = {lnewfile_path}")
        if lnewfile_path:
            newfile_path = lnewfile_path[0]
            newfile_name = os.path.basename(newfile_path)
            self.log.info(f"newfile_name = {newfile_name}")
            request.add_extracted(path, newfile_name, "resubmit")
            request.add_supplementary(path, newfile_name, "extracted file")
            text_section.add_line(f"file resubmitted as: {newfile_name}")
            self.log.info(f"file resubmitted")
            result.add_section(text_section)
        request.result = result
        