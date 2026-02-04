import re
from typing import List
from app.memory.models import ExtractedIntel

class IntelExtractor:
    UPI_REGEX = r"[\w\.\-_]+@[\w]+"
    PHONE_REGEX = r"\+?(\d{1,3})?[- .]?\(?(?:\d{2,3})\)?[- .]?\d\d\d[- .]?\d\d\d\d"
    URL_REGEX = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
    
    @classmethod
    def extract(cls, text: str, turn_number: int) -> List[ExtractedIntel]:
        intel = []
        
        # Extract UPI
        for match in re.findall(cls.UPI_REGEX, text):
            intel.append(ExtractedIntel(
                type="UPI", value=match, confidence=0.9, turn_found=turn_number
            ))
            
        # Extract URL
        for match in re.findall(cls.URL_REGEX, text):
            intel.append(ExtractedIntel(
                type="URL", value=match, confidence=0.95, turn_found=turn_number
            ))

        return intel
