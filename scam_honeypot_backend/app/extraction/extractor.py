import re
from typing import List
from app.memory.models import ExtractedIntel

class IntelExtractor:
    UPI_REGEX = r"[\w\.\-_]+@[\w]+"
    PHONE_REGEX = r"(?:\+?\d{1,3}[- .]?)?\(?\d{3}\)?[- .]?\d{3}[- .]?\d{4}|\b\d{10}\b"
    # Matches http://, https://, www., or domains ending in common TLDs like .com, .ly, etc.
    URL_REGEX = r"\b(?:https?://)?(?:www\.)?[\w-]+\.(?:com|net|org|io|ly|xyz|biz|info|in|co|me|be)\b[\w./?%&=-]*"
    
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

        # Extract PHONE
        simple_phone_matches = re.findall(r"\b\d{10}\b", text) # Capture pure 10 digits
        complex_phone_matches = re.findall(r"\+?\d{1,3}[- .]?\(?\d{3}\)?[- .]?\d{3}[- .]?\d{4}", text)
        
        all_phones = set(simple_phone_matches + complex_phone_matches)
        
        for match in all_phones:
            intel.append(ExtractedIntel(
                type="PHONE", value=match, confidence=0.8, turn_found=turn_number
            ))

        return intel
