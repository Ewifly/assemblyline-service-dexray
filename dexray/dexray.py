import os, string, tempfile, glob
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
        assert(file)
        cwd = self.working_directory
        assert(cwd)
        filename = request.file_name
        assert(filename)
        self.log.info(f"file = {file}")
        result = Result()
        text_section = ResultSection('DexRay logs :')
        text_section.add_line("after cmd")
        # my_cmd = "perl" + os.getcwd() + "dexray/dexray.pl " + request.file_path
        unquar = Popen(["perl", self.dexraytool, file])
        _ = unquar.communicate()
        text_section.add_line("after cmd")
        text_section.add_line("command success")
        self.log.info(f"command success")

        self.log.info(f"workingdir = {cwd}")
        text_section.add_line(f"workingdir = {cwd}")
        self.log.info(f"filename = {filename}")
        text_section.add_line(f"file name = {filename}")

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
        