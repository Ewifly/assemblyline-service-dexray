import os, string
from pathlib import Path

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

            for path in Path(request.file_path).glob(request.file_name + ".*"):
                request.add_extracted(request.file_path, path, str, Result, request)
                print("salut le web")
        request.result = result
        