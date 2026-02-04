import re
from typing import List

class SignalDetector:
    # Static patterns for common scam indicators
    # Note: Case sensitivity is handled by the search method
    SCAM_PATTERNS = [
        r"\burge\b",
        r"\blottery\b",
        r"\bwinner\b",
        r"\birs\b",
        r"\btax\b",
        r"\bowe\b",
        r"\bpolice\b",
        r"\barrest\b",
        r"\bverify\b",
        r"\baccount.*locked\b",
        r"\bgift.*card\b",
        r"\bbtc\b",
        r"\bcrypto\b",
        r"\binvestment\b",
        r"\breturn\b",
        r"\bwhatsapp\b",
        r"\btelegram\b",
        r"\bjob\b.*\btask\b",
        r"\bupi\b",
        r"\bpay\b",
        r"\bsend\b.*\bmoney\b",
    ]

    @classmethod
    def find_matches(cls, text: str) -> List[str]:
        matches = []
        for pattern in cls.SCAM_PATTERNS:
            # Use re.IGNORECASE flag here instead of inline (?i)
            if re.search(pattern, text, re.IGNORECASE):
                matches.append(pattern)
        return matches
