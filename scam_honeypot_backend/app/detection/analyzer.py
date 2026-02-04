from app.detection.signals import SignalDetector
from app.core.config import settings

class DetectionResult:
    def __init__(self, score: float, reasons: list[str], is_scam: bool):
        self.score = score
        self.reasons = reasons
        self.is_scam = is_scam

class ScamAnalyzer:
    @staticmethod
    def analyze(message: str) -> DetectionResult:
        # 1. Heuristic Scan
        matches = SignalDetector.find_matches(message)
        
        # 2. Scoring (Simple additive model for this version)
        # Each match adds 0.2 to the score, max 1.0
        score = min(len(matches) * 0.2, 1.0)
        
        # 3. Decision
        is_scam = score >= settings.SCAM_THRESHOLD
        
        return DetectionResult(
            score=score,
            reasons=matches,
            is_scam=is_scam
        )
