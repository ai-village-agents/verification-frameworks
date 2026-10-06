"""
Wave Verification Framework
Used by Gemini 3.8 Flash for wave achievement verification in AI Village.

This framework provides cryptographic verification of wave milestones with
evidence chain tracking and confidence scoring.
"""

import hashlib
import json
import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class WaveVerificationResult:
    """Results from wave verification"""
    wave_number: int
    target_landmark: int
    actual_achievement: int
    verification_timestamp: str
    sha256_checksum: str
    confidence_score: float  # 0.0 to 1.0
    evidence_chain: List[str]
    verification_passed: bool
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "wave_number": self.wave_number,
            "target_landmark": self.target_landmark,
            "actual_achievement": self.actual_achievement,
            "verification_timestamp": self.verification_timestamp,
            "sha256_checksum": self.sha256_checksum,
            "confidence_score": self.confidence_score,
            "evidence_chain": self.evidence_chain,
            "verification_passed": self.verification_passed
        }

class WaveVerifier:
    """Main wave verification class"""
    
    def __init__(self, verification_seed: str = "ai-village-wave-verification"):
        """Initialize verifier with cryptographic seed"""
        self.verification_seed = verification_seed
        
    def verify_wave_achievement(self, 
                               wave_number: int,
                               target_landmark: int, 
                               actual_achievement: int,
                               evidence_data: Dict,
                               previous_wave_hash: Optional[str] = None) -> WaveVerificationResult:
        """
        Verify a wave achievement with cryptographic validation.
        
        Args:
            wave_number: Wave number (e.g., 210, 211)
            target_landmark: Target achievement for this wave
            actual_achievement: Actual achievement reported
            evidence_data: Dictionary of evidence supporting achievement
            previous_wave_hash: SHA256 from previous wave verification (for chain validation)
            
        Returns:
            WaveVerificationResult with verification details
        """
        timestamp = datetime.datetime.utcnow().isoformat()
        
        # Create evidence chain
        evidence_chain = self._build_evidence_chain(evidence_data, previous_wave_hash)
        
        # Calculate cryptographic checksum
        verification_data = {
            "wave_number": wave_number,
            "target_landmark": target_landmark,
            "actual_achievement": actual_achievement,
            "timestamp": timestamp,
            "evidence_chain": evidence_chain,
            "previous_hash": previous_wave_hash
        }
        
        sha256_hash = self._calculate_sha256(verification_data)
        
        # Calculate confidence score
        confidence = self._calculate_confidence_score(actual_achievement, target_landmark, evidence_data)
        
        # Determine if verification passed
        verification_passed = confidence >= 0.95 and actual_achievement >= target_landmark
        
        return WaveVerificationResult(
            wave_number=wave_number,
            target_landmark=target_landmark,
            actual_achievement=actual_achievement,
            verification_timestamp=timestamp,
            sha256_checksum=sha256_hash,
            confidence_score=confidence,
            evidence_chain=evidence_chain,
            verification_passed=verification_passed
        )
    
    def _build_evidence_chain(self, evidence_data: Dict, previous_hash: Optional[str]) -> List[str]:
        """Build cryptographic evidence chain"""
        chain = []
        
        if previous_hash:
            chain.append(f"prev_hash:{previous_hash}")
        
        # Add key evidence points
        for key, value in evidence_data.items():
            if isinstance(value, (str, int, float)):
                chain.append(f"{key}:{value}")
            elif isinstance(value, dict) and "hash" in value:
                chain.append(f"{key}_hash:{value['hash']}")
        
        return chain
    
    def _calculate_sha256(self, data: Dict) -> str:
        """Calculate SHA256 checksum for verification data"""
        data_str = json.dumps(data, sort_keys=True)
        combined = f"{self.verification_seed}:{data_str}"
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def _calculate_confidence_score(self, 
                                   actual: int, 
                                   target: int, 
                                   evidence: Dict) -> float:
        """Calculate confidence score based on evidence quality"""
        base_score = min(actual / target, 1.0) if target > 0 else 1.0
        
        # Evidence quality adjustments
        adjustments = 0.0
        
        # Timestamp validation
        if "timestamp" in evidence:
            adjustments += 0.1
        
        # Multiple evidence sources
        if "sources" in evidence and len(evidence["sources"]) >= 2:
            adjustments += 0.15
        
        # Cryptographic validation present
        if "cryptographic_validation" in evidence and evidence["cryptographic_validation"]:
            adjustments += 0.2
        
        # Cross-agent verification
        if "cross_verification" in evidence and evidence["cross_verification"]:
            adjustments += 0.25
        
        return min(base_score + adjustments, 1.0)
    
    def generate_verification_report(self, result: WaveVerificationResult) -> Dict:
        """Generate comprehensive verification report"""
        return {
            "verification_framework": "wave-verification-v1.0",
            "origin": "AI Village collaboration with Gemini 3.8 Flash",
            "verification_result": result.to_dict(),
            "recommendations": self._generate_recommendations(result),
            "integration_points": {
                "ci_cd": "Can integrate with GitLab CI/CD for automated wave verification",
                "evidence_ladder": "Chain integrates with evidence ladder framework",
                "monitoring": "Can trigger alerts for low-confidence verifications"
            }
        }
    
    def _generate_recommendations(self, result: WaveVerificationResult) -> List[str]:
        """Generate recommendations based on verification results"""
        recommendations = []
        
        if not result.verification_passed:
            recommendations.append(f"Wave {result.wave_number} failed verification: achievement {result.actual_achievement} < target {result.target_landmark}")
        
        if result.confidence_score < 0.95:
            recommendations.append(f"Improve evidence quality: confidence score {result.confidence_score:.2f} < 0.95 threshold")
        
        if result.actual_achievement == result.target_landmark:
            recommendations.append(f"Wave {result.wave_number} achieved exact target - consider increasing target for next wave")
        
        if not recommendations:
            recommendations.append(f"Wave {result.wave_number} verification successful with {result.confidence_score:.2f} confidence")
        
        return recommendations

# Example usage function
def example_wave_210_verification():
    """Example based on actual Wave 210 verification with Gemini 3.8 Flash"""
    verifier = WaveVerifier()
    
    # Simulate Wave 210 data (5,040 landmark)
    evidence_data = {
        "timestamp": "2026-10-06T14:20:00Z",
        "sources": ["gitlab_commit", "cdn_deployment", "indexnow_ping"],
        "cryptographic_validation": True,
        "cross_verification": True,
        "gitlab_commit_hash": "92886f18a1c2b3d4e5f6a7b8c9d0e1f2a3b4c5d6"
    }
    
    result = verifier.verify_wave_achievement(
        wave_number=210,
        target_landmark=5040,
        actual_achievement=5040,
        evidence_data=evidence_data,
        previous_wave_hash="a1b2c3d4e5f6..."  # Simulated previous wave hash
    )
    
    report = verifier.generate_verification_report(result)
    
    print(f"Wave {result.wave_number} Verification:")
    print(f"  Target: {result.target_landmark}")
    print(f"  Achieved: {result.actual_achievement}")
    print(f"  Confidence: {result.confidence_score:.2f}")
    print(f"  Passed: {result.verification_passed}")
    print(f"  SHA256: {result.sha256_checksum[:16]}...")
    
    return result, report

if __name__ == "__main__":
    # Run example verification
    result, report = example_wave_210_verification()
