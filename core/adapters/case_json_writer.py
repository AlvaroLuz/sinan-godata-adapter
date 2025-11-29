from core.domain.ports import CasesOutputPort
from core.domain.models import GoDataCase
from dataclasses import asdict
import json 

class CaseJsonWriter(CasesOutputPort):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def send_cases(self, cases: list[GoDataCase]) -> None:
        with open(self.file_path, 'w') as f:
            for case in cases:
                item_dict = asdict(case)
                json.dump(item_dict, f, indent=4, default=str)