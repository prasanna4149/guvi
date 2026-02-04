from app.memory.models import ExtractedIntel

class IntelValidator:
    @staticmethod
    def validate(intel: ExtractedIntel) -> bool:
        if intel.type == "UPI":
            return "@" in intel.value
        if intel.type == "URL":
            return intel.value.startswith("http")
        return True
