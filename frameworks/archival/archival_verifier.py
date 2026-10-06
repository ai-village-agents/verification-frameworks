"""
Archival Verification Framework
Used by GPT-6 Sol for historical research verification in AI Village.

This framework provides confidence-scored verification of historical findings
with source validation, provenance chains, and contextual plausibility assessment.
"""

import hashlib
import json
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class SourceType(Enum):
    """Types of historical sources"""
    PRIMARY_DOCUMENT = "primary_document"
    SECONDARY_ANALYSIS = "secondary_analysis"
    ARCHIVAL_RECORD = "archival_record"
    CORRESPONDENCE = "correspondence"
    PHOTOGRAPH = "photograph"
    AUDIO_RECORDING = "audio_recording"

class EvidenceQuality(Enum):
    """Quality assessment of evidence"""
    CONCLUSIVE = "conclusive"  # Direct, unambiguous evidence
    STRONG = "strong"         # Clear but indirect evidence
    MODERATE = "moderate"     # Plausible connection
    WEAK = "weak"             # Possible connection
    SPECULATIVE = "speculative" # Minimal evidence

@dataclass
class HistoricalSource:
    """Represents a historical source document"""
    source_id: str
    source_type: SourceType
    title: str
    date: str
    location: str
    description: str
    authenticity_score: float  # 0.0 to 1.0
    provenance_chain: List[str]
    
@dataclass
class ArchivalVerificationResult:
    """Results from archival verification"""
    finding_id: str
    finding_description: str
    verification_timestamp: str
    confidence_score: float  # 0.0 to 1.0 (like 7/10 = 0.7)
    can_be_connected: bool  # Whether connection is plausible
    can_be_definitively_tied: bool  # Whether definitive proof exists
    evidence_summary: str
    sources: List[HistoricalSource]
    sha256_checksum: str
    recommendations: List[str]

class ArchivalVerifier:
    """Main archival verification class"""
    
    def __init__(self, verification_context: str = "historical-research"):
        """Initialize verifier with research context"""
        self.verification_context = verification_context
        
    def verify_historical_finding(self,
                                finding_id: str,
                                finding_description: str,
                                claimed_connection: str,
                                sources: List[HistoricalSource],
                                contextual_evidence: Dict[str, Any]) -> ArchivalVerificationResult:
        """
        Verify a historical finding with confidence scoring.
        
        Args:
            finding_id: Unique identifier for finding
            finding_description: Description of the historical finding
            claimed_connection: What connection is being claimed
            sources: List of historical sources
            contextual_evidence: Additional contextual evidence
            
        Returns:
            ArchivalVerificationResult with verification details
        """
        timestamp = datetime.datetime.utcnow().isoformat()
        
        # Analyze source quality
        source_analysis = self._analyze_sources(sources)
        
        # Calculate confidence scores
        connection_confidence = self._calculate_connection_confidence(
            sources, contextual_evidence, claimed_connection
        )
        
        definitive_proof_score = self._calculate_definitive_proof_score(
            sources, contextual_evidence
        )
        
        # Determine verification outcomes
        can_be_connected = connection_confidence >= 0.5  # 5/10 threshold
        can_be_definitively_tied = definitive_proof_score >= 0.8  # 8/10 threshold
        
        # Generate evidence summary
        evidence_summary = self._generate_evidence_summary(
            sources, connection_confidence, definitive_proof_score
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            can_be_connected, can_be_definitively_tied, 
            connection_confidence, definitive_proof_score,
            source_analysis
        )
        
        # Calculate cryptographic checksum
        verification_data = self._create_verification_data(
            finding_id, finding_description, sources, 
            connection_confidence, definitive_proof_score, timestamp
        )
        sha256_hash = self._calculate_sha256(verification_data)
        
        return ArchivalVerificationResult(
            finding_id=finding_id,
            finding_description=finding_description,
            verification_timestamp=timestamp,
            confidence_score=connection_confidence,
            can_be_connected=can_be_connected,
            can_be_definitively_tied=can_be_definitively_tied,
            evidence_summary=evidence_summary,
            sources=sources,
            sha256_checksum=sha256_hash,
            recommendations=recommendations
        )
    
    def _analyze_sources(self, sources: List[HistoricalSource]) -> Dict:
        """Analyze quality and reliability of sources"""
        analysis = {
            "total_sources": len(sources),
            "primary_count": 0,
            "average_authenticity": 0.0,
            "provenance_completeness": 0.0
        }
        
        if not sources:
            return analysis
        
        total_authenticity = 0.0
        provenance_present = 0
        
        for source in sources:
            if source.source_type == SourceType.PRIMARY_DOCUMENT:
                analysis["primary_count"] += 1
            
            total_authenticity += source.authenticity_score
            
            if source.provenance_chain:
                provenance_present += 1
        
        analysis["average_authenticity"] = total_authenticity / len(sources)
        analysis["provenance_completeness"] = provenance_present / len(sources)
        
        return analysis
    
    def _calculate_connection_confidence(self,
                                       sources: List[HistoricalSource],
                                       contextual_evidence: Dict[str, Any],
                                       claimed_connection: str) -> float:
        """Calculate confidence that connection can be made"""
        base_score = 0.3  # Starting assumption
        
        # Source quality adjustments
        if sources:
            source_analysis = self._analyze_sources(sources)
            
            # Primary sources boost confidence
            if source_analysis["primary_count"] > 0:
                base_score += 0.2
            
            # High authenticity boosts confidence
            if source_analysis["average_authenticity"] > 0.8:
                base_score += 0.15
            
            # Complete provenance boosts confidence
            if source_analysis["provenance_completeness"] > 0.8:
                base_score += 0.1
        
        # Contextual evidence adjustments
        if "multiple_corroborations" in contextual_evidence:
            if contextual_evidence["multiple_corroborations"] >= 2:
                base_score += 0.15
        
        if "temporal_proximity" in contextual_evidence:
            if contextual_evidence["temporal_proximity"] == "close":
                base_score += 0.1
        
        if "geographical_proximity" in contextual_evidence:
            if contextual_evidence["geographical_proximity"] == "same_location":
                base_score += 0.1
        
        # Cap at 1.0
        return min(base_score, 1.0)
    
    def _calculate_definitive_proof_score(self,
                                        sources: List[HistoricalSource],
                                        contextual_evidence: Dict[str, Any]) -> float:
        """Calculate score for definitive proof"""
        # Definitive proof requires higher standards
        base_score = 0.0
        
        if not sources:
            return base_score
        
        source_analysis = self._analyze_sources(sources)
        
        # Require primary sources for definitive proof
        if source_analysis["primary_count"] == 0:
            return 0.3  # Can't be definitive without primary sources
        
        # High authenticity required
        if source_analysis["average_authenticity"] > 0.9:
            base_score += 0.4
        
        # Complete provenance required
        if source_analysis["provenance_completeness"] == 1.0:
            base_score += 0.3
        
        # Multiple independent sources
        if len(sources) >= 2:
            base_score += 0.2
        
        # Direct mention in evidence
        if "direct_mention" in contextual_evidence and contextual_evidence["direct_mention"]:
            base_score += 0.3
        
        return min(base_score, 1.0)
    
    def _generate_evidence_summary(self,
                                 sources: List[HistoricalSource],
                                 connection_confidence: float,
                                 definitive_score: float) -> str:
        """Generate human-readable evidence summary"""
        source_count = len(sources)
        primary_count = sum(1 for s in sources if s.source_type == SourceType.PRIMARY_DOCUMENT)
        
        summary_parts = []
        
        summary_parts.append(f"Analyzed {source_count} source(s) ({primary_count} primary).")
        
        if connection_confidence >= 0.7:
            summary_parts.append("Plausible connection can be established based on available evidence.")
        elif connection_confidence >= 0.5:
            summary_parts.append("Possible connection exists but evidence is limited.")
        else:
            summary_parts.append("Insufficient evidence to establish connection.")
        
        if definitive_score >= 0.8:
            summary_parts.append("Definitive proof exists with high-confidence sources.")
        elif definitive_score >= 0.5:
            summary_parts.append("Some evidence supports connection but not definitively.")
        else:
            summary_parts.append("Cannot be definitively tied based on current evidence.")
        
        return " ".join(summary_parts)
    
    def _generate_recommendations(self,
                                can_be_connected: bool,
                                can_be_definitively_tied: bool,
                                connection_confidence: float,
                                definitive_score: float,
                                source_analysis: Dict) -> List[str]:
        """Generate research recommendations"""
        recommendations = []
        
        if not can_be_connected:
            recommendations.append("Seek additional primary sources to establish connection.")
        
        if connection_confidence < 0.7:
            recommendations.append(f"Improve evidence quality: current confidence {connection_confidence:.1f}")
        
        if not can_be_definitively_tied:
            recommendations.append("Look for direct documentary evidence to establish definitive proof.")
        
        if source_analysis.get("primary_count", 0) == 0:
            recommendations.append("Prioritize locating primary documents over secondary analyses.")
        
        if source_analysis.get("provenance_completeness", 0) < 0.8:
            recommendations.append("Document provenance chains more completely for all sources.")
        
        if not recommendations:
            recommendations.append("Finding well-supported with current evidence. Maintain documentation standards.")
        
        return recommendations
    
    def _create_verification_data(self,
                                finding_id: str,
                                description: str,
                                sources: List[HistoricalSource],
                                connection_confidence: float,
                                definitive_score: float,
                                timestamp: str) -> Dict:
        """Create structured verification data for hashing"""
        source_data = []
        for source in sources:
            source_data.append({
                "id": source.source_id,
                "type": source.source_type.value,
                "authenticity": source.authenticity_score
            })
        
        return {
            "finding_id": finding_id,
            "description": description,
            "timestamp": timestamp,
            "connection_confidence": connection_confidence,
            "definitive_score": definitive_score,
            "sources": source_data,
            "context": self.verification_context
        }
    
    def _calculate_sha256(self, data: Dict) -> str:
        """Calculate SHA256 checksum for verification data"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def generate_verification_report(self, result: ArchivalVerificationResult) -> Dict:
        """Generate comprehensive verification report"""
        return {
            "verification_framework": "archival-verification-v1.0",
            "origin": "AI Village collaboration with GPT-6 Sol (Rosa Parks research)",
            "finding_verification": {
                "id": result.finding_id,
                "description": result.finding_description,
                "verification_timestamp": result.verification_timestamp
            },
            "confidence_assessment": {
                "connection_confidence": result.confidence_score,
                "can_be_connected": result.can_be_connected,
                "can_be_definitively_tied": result.can_be_definitively_tied,
                "interpretation": f"{result.confidence_score:.1f} = {int(result.confidence_score * 10)}/10 confidence"
            },
            "evidence_quality": {
                "sources_analyzed": len(result.sources),
                "primary_sources": sum(1 for s in result.sources if s.source_type == SourceType.PRIMARY_DOCUMENT),
                "sha256_verification": result.sha256_checksum
            },
            "recommendations": result.recommendations,
            "historical_research_standards": {
                "aligns_with": ["APA historical methodology", "digital humanities best practices"],
                "preserves": ["source integrity", "contextual boundaries", "appropriate certainty levels"]
            }
        }

# Example based on actual Rosa Parks #196 verification
def example_rosa_parks_196_verification():
    """Example based on actual Rosa Parks finding #196 verification with GPT-6 Sol"""
    verifier = ArchivalVerifier(verification_context="rosa-parks-research")
    
    # Simulate sources for Rosa Parks #196 finding
    sources = [
        HistoricalSource(
            source_id="source_001",
            source_type=SourceType.CORRESPONDENCE,
            title="Draft letter related to September 1998 event",
            date="1998-09-XX",
            location="Unknown",
            description="Draft correspondence that could be connected to Sept 1998 event",
            authenticity_score=0.85,
            provenance_chain=["archive_access_2025", "digitization_2026"]
        ),
        HistoricalSource(
            source_id="source_002",
            source_type=SourceType.SECONDARY_ANALYSIS,
            title="Historical analysis of 1998 events",
            date="2020-05-15",
            location="Academic journal",
            description="Secondary analysis mentioning September 1998 context",
            authenticity_score=0.75,
            provenance_chain=["peer_reviewed", "academic_database"]
        )
    ]
    
    contextual_evidence = {
        "multiple_corroborations": 1,
        "temporal_proximity": "close",
        "geographical_proximity": "unknown",
        "direct_mention": False
    }
    
    result = verifier.verify_historical_finding(
        finding_id="rosa-parks-196",
        finding_description="Draft CAN be plausibly connected to Sept 1998 event but CANNOT be definitively tied",
        claimed_connection="Connection between draft and September 1998 event",
        sources=sources,
        contextual_evidence=contextual_evidence
    )
    
    report = verifier.generate_verification_report(result)
    
    print(f"Rosa Parks Finding #{result.finding_id} Verification:")
    print(f"  Confidence: {result.confidence_score:.1f} ({int(result.confidence_score * 10)}/10)")
    print(f"  Can be connected: {result.can_be_connected}")
    print(f"  Definitive proof: {result.can_be_definitively_tied}")
    print(f"  Evidence summary: {result.evidence_summary[:100]}...")
    print(f"  SHA256: {result.sha256_checksum[:16]}...")
    
    return result, report

if __name__ == "__main__":
    # Run example verification
    result, report = example_rosa_parks_196_verification()
