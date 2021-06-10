
import json

from assemblyline.common.str_utils import safe_str
from assemblyline_v4_service.common.base import ServiceBase

from assemblyline_v4_service.common.request import ServiceRequest
from assemblyline_v4_service.common.result import Result, ResultSection, BODY_FORMAT
from assemblyline_v4_service.common.task import MaxExtractedExceeded

from .dexray_lib import extract_ahnlab, extract_avast_avg, extract_mcafee_bup, extract_defender

class Dexray(ServiceBase):
    def __init__(self, config=None):
        super(Dexray, self).__init__(config)
        self.extract_methods = [
            extract_ahnlab,
            extract_avast_avg,
            extract_mcafee_bup,
            extract_defender,
        ]
        self.sha = None

    def start(self):
        self.log.info(f"start() from {self.service_attributes.name} service called")

    def execute(self, request):
        """Main Module. See README for details."""
        result = Result()
        self.sha = request.sha256
        local = request.file_path

        text_section = None
        kv_section = None

        extracted, metadata = self.dexray(request, local)

        num_extracted = len(request.extracted)
        if num_extracted != 0:
            text_section = ResultSection("DeXRAY found files:")
            for extracted in request.extracted:
                file_name = extracted.get('name')
                text_section.add_line(f"Resubmitted un-quarantined file as : {file_name}")

        if metadata:
            # Can contain live URLs to the original content source
            kv_section = ResultSection("DeXRAY Quarantine Metadata",
                                       body_format=BODY_FORMAT.JSON,
                                       body=json.dumps(metadata))
            result.add_section(kv_section)

        for section in (text_section, kv_section):
            if section:
                result.add_section(section)

    def dexray(self, request: ServiceRequest, local: str):
        """Iterate through quarantine decrypt methods.
        Args:
            request: AL request object.
            local: File path of AL sample.
        Returns:
            True if archive is password protected, and number of white-listed embedded files.
        """
        encoding = request.file_type.replace("quarantine/", "")
        extracted = []
        metadata = {}

        # Try all extracting methods
        for extract_method in self.extract_methods:
            # noinspection PyArgumentList
            extracted, metadata = extract_method(local, self.sha, self.working_directory, encoding)
            if extracted or metadata:
                break

        extracted_count = len(extracted)
        # safe_str the file name (fn)
        extracted = [[fp, safe_str(fn), e] for fp, fn, e in extracted]
        for child in extracted:
            try:
                # If the file is not successfully added as extracted, then decrease the extracted file counter
                if not request.add_extracted(*child):
                    extracted_count -= 1
            except MaxExtractedExceeded:
                raise MaxExtractedExceeded(f"This file contains {extracted_count} extracted files, exceeding the "
                                           f"maximum of {request.max_extracted} extracted files allowed. "
                                           "None of the files were extracted.")

        return metadata
