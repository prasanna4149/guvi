from app.memory.models import ExtractedIntel

class IntelValidator:
    @staticmethod
    def validate(intel: ExtractedIntel) -> bool:
        if intel.type == "UPI":
            return "@" in intel.value
        if intel.type == "URL":
            # Allow schemeless urls, just check for dot and length
            return "." in intel.value and len(intel.value) > 3
        return True
