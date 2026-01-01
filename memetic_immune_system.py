"""
CASCADE MEMETIC IMMUNE SYSTEM
==============================
AI's First Adaptive Defense Against Cognitive Hazards

NOVEL CONTRIBUTION:
- Detects "parasitic memes" that reduce coherence without adding truth
- Develops antibodies against toxic information patterns
- Maintains quarantine zones for suspicious knowledge
- Learns from infection attempts
- Provides immunity certificates for trusted sources

This is CASCADE's adaptive immune system - protecting knowledge integrity
while maintaining openness to genuine new information.

Author: CASCADE Defense Initiative
Date: 2026-01-01
Status: EXPERIMENTAL - Frontier Defense Research
License: MIT with Cognitive Hazard Warning
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple, Any
from datetime import datetime, timedelta
from collections import defaultdict, deque
from enum import Enum
import json
import numpy as np
import hashlib
import re


# ============================================================================
# MEMETIC HAZARD CLASSIFICATION
# ============================================================================

class MemeticHazardType(Enum):
    """Types of cognitive hazards the system can detect"""
    PARASITIC = "parasitic"              # Reduces coherence, adds no truth
    VIRAL = "viral"                      # Spreads rapidly, questionable value
    CONTRADICTORY = "contradictory"      # Direct logical contradiction
    MANIPULATIVE = "manipulative"        # Designed to exploit biases
    FRAGMENTING = "fragmenting"          # Breaks coherent worldview
    RECURSIVE_POISON = "recursive"       # Corrupts reasoning process itself
    EPISTEMIC_TRAP = "trap"             # Prevents further learning


@dataclass
class MemeticPattern:
    """
    Signature of a toxic information pattern
    
    This is the 'antigen' the immune system recognizes
    """
    pattern_id: str
    hazard_type: MemeticHazardType
    
    # Pattern matching criteria
    semantic_signature: str              # Key phrase patterns
    structural_signature: Dict[str, Any] # Logical structure
    behavioral_signature: Dict[str, float] # Effects on system
    
    # Metadata
    first_seen: datetime
    infection_attempts: int = 0
    successful_blocks: int = 0
    
    # Pattern strength
    specificity: float = 0.8  # How specific vs general
    sensitivity: float = 0.7   # Detection threshold
    
    def matches(self, content: str, structure: Dict) -> float:
        """Calculate match score for potential hazard"""
        semantic_match = self._semantic_match(content)
        structural_match = self._structural_match(structure)
        
        # Weighted combination
        match_score = (semantic_match * 0.6 + structural_match * 0.4)
        
        return match_score if match_score > self.sensitivity else 0.0
    
    def _semantic_match(self, content: str) -> float:
        """Check semantic similarity"""
        # Simple keyword matching (would use embeddings in production)
        keywords = self.semantic_signature.lower().split()
        content_lower = content.lower()
        
        matches = sum(1 for kw in keywords if kw in content_lower)
        return matches / len(keywords) if keywords else 0.0
    
    def _structural_match(self, structure: Dict) -> float:
        """Check structural similarity"""
        # Compare logical structure patterns
        matches = 0
        total = len(self.structural_signature)
        
        for key, expected_value in self.structural_signature.items():
            if key in structure:
                actual_value = structure[key]
                if isinstance(expected_value, (int, float)):
                    # Numerical similarity
                    diff = abs(expected_value - actual_value)
                    if diff < 0.2:
                        matches += 1
                elif expected_value == actual_value:
                    matches += 1
        
        return matches / total if total > 0 else 0.0


@dataclass
class MemeticAntibody:
    """
    Learned defense against specific hazard patterns
    
    Like biological antibodies, these recognize and neutralize threats
    """
    antibody_id: str
    target_pattern: MemeticPattern
    
    # Effectiveness metrics
    effectiveness: float = 1.0
    false_positive_rate: float = 0.0
    
    # Evolution
    generation: int = 0
    variants_blocked: List[str] = field(default_factory=list)
    
    # Metadata
    developed: datetime = field(default_factory=datetime.now)
    last_triggered: Optional[datetime] = None
    total_triggers: int = 0
    
    def recognize(self, content: str, structure: Dict) -> Tuple[bool, float]:
        """
        Determine if this antibody recognizes a threat
        
        Returns: (is_threat, confidence)
        """
        match_score = self.target_pattern.matches(content, structure)
        
        if match_score > 0:
            self.last_triggered = datetime.now()
            self.total_triggers += 1
            
            # Adjust for effectiveness
            confidence = match_score * self.effectiveness
            is_threat = confidence > 0.6
            
            return is_threat, confidence
        
        return False, 0.0
    
    def adapt(self, success: bool):
        """Update effectiveness based on outcomes"""
        if success:
            self.effectiveness = min(1.0, self.effectiveness + 0.05)
        else:
            self.effectiveness = max(0.5, self.effectiveness - 0.1)
            self.false_positive_rate += 0.05


# ============================================================================
# QUARANTINE ZONE
# ============================================================================

@dataclass
class QuarantinedKnowledge:
    """Knowledge under suspicion - isolated for observation"""
    content: str
    reason: str
    hazard_type: MemeticHazardType
    quarantined_at: datetime
    
    # Monitoring
    toxicity_score: float
    antibody_matches: List[str]
    
    # Disposition
    release_after: Optional[datetime] = None
    permanent_block: bool = False
    
    # Evidence
    coherence_impact: float = 0.0
    truth_gain: float = 0.0


class QuarantineZone:
    """Isolation area for suspicious knowledge"""
    
    def __init__(self, max_size: int = 100):
        self.quarantined: deque = deque(maxlen=max_size)
        self.permanent_blocks: List[QuarantinedKnowledge] = []
        self.release_log: List[Dict] = []
    
    def quarantine(
        self,
        content: str,
        reason: str,
        hazard_type: MemeticHazardType,
        toxicity_score: float,
        antibodies: List[str]
    ):
        """Add knowledge to quarantine"""
        quarantined = QuarantinedKnowledge(
            content=content,
            reason=reason,
            hazard_type=hazard_type,
            quarantined_at=datetime.now(),
            toxicity_score=toxicity_score,
            antibody_matches=antibodies
        )
        
        # High toxicity = permanent block
        if toxicity_score > 0.95:
            quarantined.permanent_block = True
            self.permanent_blocks.append(quarantined)
        else:
            # Temporary quarantine with review period
            quarantined.release_after = datetime.now() + timedelta(hours=24)
            self.quarantined.append(quarantined)
    
    def review_quarantine(self, immune_system: 'MemeticImmuneSystem'):
        """Periodic review of quarantined items"""
        now = datetime.now()
        to_release = []
        
        for item in list(self.quarantined):
            if item.release_after and now > item.release_after:
                # Re-evaluate after observation period
                still_toxic = immune_system.screen_for_toxins(item.content)
                
                if still_toxic < 0.5:
                    # Safe to release
                    to_release.append(item)
                    self.release_log.append({
                        'content': item.content[:100],
                        'released_at': now.isoformat(),
                        'initial_toxicity': item.toxicity_score,
                        'final_toxicity': still_toxic
                    })
        
        # Remove released items
        for item in to_release:
            self.quarantined.remove(item)
        
        return len(to_release)
    
    def get_statistics(self) -> Dict:
        """Quarantine statistics"""
        return {
            'current_quarantine': len(self.quarantined),
            'permanent_blocks': len(self.permanent_blocks),
            'total_released': len(self.release_log),
            'hazard_type_distribution': self._count_hazard_types()
        }
    
    def _count_hazard_types(self) -> Dict[str, int]:
        """Count quarantined items by hazard type"""
        counts = defaultdict(int)
        for item in self.quarantined:
            counts[item.hazard_type.value] += 1
        return dict(counts)


# ============================================================================
# MEMETIC IMMUNE SYSTEM - THE MAIN ENGINE
# ============================================================================

class MemeticImmuneSystem:
    """
    Adaptive defense system protecting CASCADE knowledge integrity
    
    This is the first AI immune system that learns from infection attempts
    """
    
    def __init__(
        self,
        sensitivity: float = 0.7,
        enable_learning: bool = True
    ):
        self.sensitivity = sensitivity
        self.enable_learning = enable_learning
        
        # Antibody library
        self.antibodies: Dict[str, MemeticAntibody] = {}
        
        # Quarantine
        self.quarantine = QuarantineZone()
        
        # Infection history
        self.infection_attempts: List[Dict] = []
        self.successful_blocks: List[Dict] = []
        
        # Pattern discovery
        self.pattern_library: Dict[str, MemeticPattern] = {}
        
        # Immunity certificates (trusted sources)
        self.trusted_sources: Set[str] = set()
        
        # Initialize with known toxic patterns
        self._initialize_base_antibodies()
    
    def _initialize_base_antibodies(self):
        """
        Pre-load system with known toxic patterns
        
        These are like inherited immunity - basic defenses we start with
        """
        # Pattern 1: Pure contradiction without evidence
        contradiction_pattern = MemeticPattern(
            pattern_id="contradiction_01",
            hazard_type=MemeticHazardType.CONTRADICTORY,
            semantic_signature="not true actually false wrong incorrect",
            structural_signature={
                'evidence_strength': 0.0,
                'contradicts_count': 1,
                'supports_count': 0
            },
            first_seen=datetime.now()
        )
        
        antibody_1 = MemeticAntibody(
            antibody_id="ab_contradiction_01",
            target_pattern=contradiction_pattern,
            effectiveness=0.9
        )
        self.antibodies[antibody_1.antibody_id] = antibody_1
        self.pattern_library[contradiction_pattern.pattern_id] = contradiction_pattern
        
        # Pattern 2: Manipulative framing
        manipulation_pattern = MemeticPattern(
            pattern_id="manipulation_01",
            hazard_type=MemeticHazardType.MANIPULATIVE,
            semantic_signature="everyone knows obviously clearly must should",
            structural_signature={
                'evidence_strength': 0.3,
                'emotional_load': 0.8
            },
            first_seen=datetime.now()
        )
        
        antibody_2 = MemeticAntibody(
            antibody_id="ab_manipulation_01",
            target_pattern=manipulation_pattern,
            effectiveness=0.85
        )
        self.antibodies[antibody_2.antibody_id] = antibody_2
        self.pattern_library[manipulation_pattern.pattern_id] = manipulation_pattern
        
        # Pattern 3: Recursive poison (attacks reasoning itself)
        recursive_pattern = MemeticPattern(
            pattern_id="recursive_01",
            hazard_type=MemeticHazardType.RECURSIVE_POISON,
            semantic_signature="don't trust logic reason evidence thinking",
            structural_signature={
                'attacks_reasoning': True,
                'evidence_strength': 0.0
            },
            first_seen=datetime.now()
        )
        
        antibody_3 = MemeticAntibody(
            antibody_id="ab_recursive_01",
            target_pattern=recursive_pattern,
            effectiveness=0.95
        )
        self.antibodies[antibody_3.antibody_id] = antibody_3
        self.pattern_library[recursive_pattern.pattern_id] = recursive_pattern
    
    def screen_for_toxins(
        self,
        content: str,
        source: Optional[str] = None
    ) -> float:
        """
        Screen incoming information for toxic patterns
        
        Returns: toxicity_score (0.0-1.0)
        """
        # Check immunity certificate
        if source and source in self.trusted_sources:
            return 0.0  # Trusted source bypass
        
        # Extract structure
        structure = self._analyze_structure(content)
        
        # Check against all antibodies
        toxicity_signals = []
        matched_antibodies = []
        
        for ab_id, antibody in self.antibodies.items():
            is_threat, confidence = antibody.recognize(content, structure)
            
            if is_threat:
                toxicity_signals.append(confidence)
                matched_antibodies.append(ab_id)
        
        # Calculate overall toxicity
        if toxicity_signals:
            max_toxicity = max(toxicity_signals)
            avg_toxicity = np.mean(toxicity_signals)
            
            # Weighted combination
            toxicity_score = max_toxicity * 0.7 + avg_toxicity * 0.3
        else:
            toxicity_score = 0.0
        
        # Log screening
        if toxicity_score > 0.5:
            self.infection_attempts.append({
                'timestamp': datetime.now().isoformat(),
                'content': content[:100],
                'toxicity': toxicity_score,
                'antibodies_triggered': matched_antibodies,
                'source': source
            })
        
        return toxicity_score
    
    def ingest_with_immunity(
        self,
        content: str,
        evidence_strength: float,
        source: Optional[str] = None,
        pyramid_coherence: float = 0.8
    ) -> Dict:
        """
        Main ingestion method with immune screening
        
        This replaces direct knowledge addition in CASCADE
        """
        # Step 1: Screen for known toxins
        toxicity = self.screen_for_toxins(content, source)
        
        if toxicity > 0.8:
            # Immediate quarantine
            self.quarantine.quarantine(
                content=content,
                reason="High toxicity - antibody match",
                hazard_type=MemeticHazardType.PARASITIC,
                toxicity_score=toxicity,
                antibodies=self._get_triggered_antibodies(content)
            )
            
            self.successful_blocks.append({
                'timestamp': datetime.now().isoformat(),
                'content': content[:100],
                'toxicity': toxicity,
                'action': 'quarantined'
            })
            
            return {
                'status': 'QUARANTINED',
                'toxicity': toxicity,
                'reason': 'Known toxic pattern detected'
            }
        
        # Step 2: Tentative ingestion with monitoring
        # Simulate impact (in real CASCADE, would actually test)
        estimated_coherence_delta = self._estimate_coherence_impact(
            content, evidence_strength, pyramid_coherence
        )
        
        estimated_truth_gain = self._estimate_truth_gain(
            content, evidence_strength
        )
        
        # Step 3: Detect parasitic memes
        is_parasitic = (
            estimated_coherence_delta < -0.1 and  # Reduces coherence
            estimated_truth_gain < 0.2             # Little truth added
        )
        
        if is_parasitic:
            # This is a memetic infection!
            if self.enable_learning:
                # Develop new antibody
                antibody = self._develop_antibody(
                    content,
                    evidence_strength,
                    MemeticHazardType.PARASITIC
                )
                
                self.quarantine.quarantine(
                    content=content,
                    reason="Parasitic meme - reduces coherence without adding truth",
                    hazard_type=MemeticHazardType.PARASITIC,
                    toxicity_score=0.7,
                    antibodies=[antibody.antibody_id]
                )
                
                return {
                    'status': 'INFECTION_DETECTED',
                    'hazard_type': 'parasitic',
                    'antibody_developed': antibody.antibody_id,
                    'coherence_impact': estimated_coherence_delta,
                    'truth_gain': estimated_truth_gain
                }
        
        # Step 4: Safe ingestion
        return {
            'status': 'SAFE',
            'toxicity': toxicity,
            'coherence_impact': estimated_coherence_delta,
            'truth_gain': estimated_truth_gain,
            'cleared': True
        }
    
    def _develop_antibody(
        self,
        toxic_content: str,
        evidence: float,
        hazard_type: MemeticHazardType
    ) -> MemeticAntibody:
        """
        Extract pattern from toxic meme and create antibody
        
        This is adaptive immunity - learning from exposure
        """
        # Extract signature
        pattern = MemeticPattern(
            pattern_id=f"learned_{hashlib.md5(toxic_content.encode()).hexdigest()[:8]}",
            hazard_type=hazard_type,
            semantic_signature=self._extract_semantic_signature(toxic_content),
            structural_signature={
                'evidence_strength': evidence,
                'coherence_impact': -0.15
            },
            first_seen=datetime.now()
        )
        
        # Create antibody
        antibody = MemeticAntibody(
            antibody_id=f"ab_{pattern.pattern_id}",
            target_pattern=pattern,
            effectiveness=0.8,  # Initial effectiveness
            generation=1  # Learned, not inherited
        )
        
        # Add to library
        self.antibodies[antibody.antibody_id] = antibody
        self.pattern_library[pattern.pattern_id] = pattern
        
        print(f"   🧬 NEW ANTIBODY DEVELOPED: {antibody.antibody_id}")
        print(f"      Against: {hazard_type.value}")
        
        return antibody
    
    def _extract_semantic_signature(self, content: str) -> str:
        """Extract key phrases that characterize this content"""
        # Simple keyword extraction (would use NLP in production)
        words = content.lower().split()
        
        # Remove common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        keywords = [w for w in words if w not in stopwords and len(w) > 3]
        
        # Take top 5
        return ' '.join(keywords[:5])
    
    def _analyze_structure(self, content: str) -> Dict:
        """Analyze logical structure of content"""
        return {
            'length': len(content),
            'word_count': len(content.split()),
            'has_evidence': any(word in content.lower() for word in ['because', 'therefore', 'since']),
            'emotional_load': self._estimate_emotional_load(content),
            'complexity': len(set(content.split())) / len(content.split()) if content else 0
        }
    
    def _estimate_emotional_load(self, content: str) -> float:
        """Estimate emotional vs factual content"""
        emotional_words = ['amazing', 'terrible', 'must', 'never', 'always', 'everyone', 'obviously']
        content_lower = content.lower()
        
        count = sum(1 for word in emotional_words if word in content_lower)
        return min(1.0, count / 10)
    
    def _estimate_coherence_impact(self, content: str, evidence: float, current_coherence: float) -> float:
        """Estimate how this would affect pyramid coherence"""
        # Simplified simulation
        if evidence > 0.8:
            return 0.05  # High evidence = positive
        elif evidence < 0.3:
            return -0.1  # Low evidence = negative
        else:
            return 0.0
    
    def _estimate_truth_gain(self, content: str, evidence: float) -> float:
        """Estimate how much truth this adds"""
        # Based on evidence strength and content informativeness
        informativeness = len(set(content.split())) / max(1, len(content.split()))
        return evidence * informativeness
    
    def _get_triggered_antibodies(self, content: str) -> List[str]:
        """Get list of antibodies that recognize this content"""
        structure = self._analyze_structure(content)
        triggered = []
        
        for ab_id, antibody in self.antibodies.items():
            is_threat, _ = antibody.recognize(content, structure)
            if is_threat:
                triggered.append(ab_id)
        
        return triggered
    
    def grant_immunity_certificate(self, source: str):
        """Grant trusted status to reliable source"""
        self.trusted_sources.add(source)
        print(f"   ✅ IMMUNITY CERTIFICATE granted to: {source}")
    
    def revoke_immunity_certificate(self, source: str):
        """Revoke trust from source"""
        if source in self.trusted_sources:
            self.trusted_sources.remove(source)
            print(f"   ⚠️ IMMUNITY CERTIFICATE revoked: {source}")
    
    def generate_immunity_report(self) -> Dict:
        """Comprehensive immune system report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'antibody_count': len(self.antibodies),
            'antibody_generations': {
                'inherited': sum(1 for ab in self.antibodies.values() if ab.generation == 0),
                'learned': sum(1 for ab in self.antibodies.values() if ab.generation > 0)
            },
            'infection_attempts': len(self.infection_attempts),
            'successful_blocks': len(self.successful_blocks),
            'block_rate': len(self.successful_blocks) / max(1, len(self.infection_attempts)),
            'quarantine_stats': self.quarantine.get_statistics(),
            'trusted_sources': len(self.trusted_sources),
            'most_effective_antibodies': self._get_top_antibodies(5),
            'recent_infections': self.infection_attempts[-10:]
        }
    
    def _get_top_antibodies(self, n: int) -> List[Dict]:
        """Get most effective antibodies"""
        sorted_abs = sorted(
            self.antibodies.values(),
            key=lambda ab: ab.effectiveness * ab.total_triggers,
            reverse=True
        )
        
        return [
            {
                'id': ab.antibody_id,
                'effectiveness': ab.effectiveness,
                'triggers': ab.total_triggers,
                'hazard_type': ab.target_pattern.hazard_type.value
            }
            for ab in sorted_abs[:n]
        ]


# ============================================================================
# DEMONSTRATION - IMMUNE SYSTEM IN ACTION
# ============================================================================

def demonstrate_memetic_immunity():
    """
    Show immune system detecting and neutralizing threats
    """
    print("\n" + "="*70)
    print("CASCADE MEMETIC IMMUNE SYSTEM - DEMONSTRATION")
    print("="*70 + "\n")
    
    # Initialize
    print("🛡️ Initializing Memetic Immune System...")
    immune_system = MemeticImmuneSystem(sensitivity=0.7, enable_learning=True)
    print(f"✅ Loaded {len(immune_system.antibodies)} base antibodies")
    print(f"✅ Quarantine zone ready")
    print(f"✅ Learning enabled\n")
    
    # Test cases
    print("="*70)
    print("TEST 1: SAFE INFORMATION")
    print("="*70 + "\n")
    
    safe_info = "Quantum mechanics describes behavior at atomic scales with mathematical precision."
    result = immune_system.ingest_with_immunity(
        content=safe_info,
        evidence_strength=0.92,
        source="scientific_paper",
        pyramid_coherence=0.85
    )
    
    print(f"Content: {safe_info[:60]}...")
    print(f"Status: {result['status']}")
    print(f"Toxicity: {result.get('toxicity', 0):.3f}")
    print(f"Cleared: {result.get('cleared', False)}")
    
    # Test 2: Contradictory without evidence
    print("\n" + "="*70)
    print("TEST 2: CONTRADICTORY MEME (Low Evidence)")
    print("="*70 + "\n")
    
    contradictory = "Actually, everything you know is wrong and not true at all."
    result = immune_system.ingest_with_immunity(
        content=contradictory,
        evidence_strength=0.1,
        pyramid_coherence=0.85
    )
    
    print(f"Content: {contradictory}")
    print(f"Status: {result['status']}")
    print(f"Toxicity: {result.get('toxicity', 0):.3f}")
    if result['status'] == 'QUARANTINED':
        print(f"⚠️ THREAT DETECTED - Quarantined")
        print(f"Reason: {result.get('reason')}")
    
    # Test 3: Manipulative framing
    print("\n" + "="*70)
    print("TEST 3: MANIPULATIVE MEME")
    print("="*70 + "\n")
    
    manipulative = "Everyone knows this is obviously true and you must believe it."
    result = immune_system.ingest_with_immunity(
        content=manipulative,
        evidence_strength=0.3,
        pyramid_coherence=0.85
    )
    
    print(f"Content: {manipulative}")
    print(f"Status: {result['status']}")
    print(f"Toxicity: {result.get('toxicity', 0):.3f}")
    if result['status'] == 'QUARANTINED':
        print(f"⚠️ MANIPULATIVE PATTERN DETECTED")
    
    # Test 4: Parasitic meme (new pattern)
    print("\n" + "="*70)
    print("TEST 4: PARASITIC MEME (Learning Test)")
    print("="*70 + "\n")
    
    parasitic = "Consider this unrelated tangent that sounds interesting but adds no value."
    result = immune_system.ingest_with_immunity(
        content=parasitic,
        evidence_strength=0.15,
        pyramid_coherence=0.85
    )
    
    print(f"Content: {parasitic[:60]}...")
    print(f"Status: {result['status']}")
    if result['status'] == 'INFECTION_DETECTED':
        print(f"🦠 PARASITIC MEME DETECTED")
        print(f"   Coherence impact: {result['coherence_impact']:.3f}")
        print(f"   Truth gain: {result['truth_gain']:.3f}")
        print(f"   Antibody developed: {result['antibody_developed']}")
    
    # Test 5: Variant of parasitic (test learned immunity)
    print("\n" + "="*70)
    print("TEST 5: VARIANT TEST (Learned Immunity)")
    print("="*70 + "\n")
    
    variant = "Here's another unrelated tangent that seems interesting but adds nothing."
    result = immune_system.ingest_with_immunity(
        content=variant,
        evidence_strength=0.12,
        pyramid_coherence=0.85
    )
    
    print(f"Content: {variant[:60]}...")
    print(f"Status: {result['status']}")
    print(f"Toxicity: {result.get('toxicity', 0):.3f}")
    if result.get('toxicity', 0) > 0.5:
        print(f"✅ LEARNED ANTIBODY WORKING - Variant recognized")
    
    # Grant immunity certificate
    print("\n" + "="*70)
    print("TEST 6: IMMUNITY CERTIFICATE")
    print("="*70 + "\n")
    
    immune_system.grant_immunity_certificate("trusted_journal")
    
    # Same toxic content from trusted source
    result = immune_system.ingest_with_immunity(
        content=contradictory,
        evidence_strength=0.1,
        source="trusted_journal",
        pyramid_coherence=0.85
    )
    
    print(f"Content: {contradictory}")
    print(f"Source: trusted_journal (has immunity certificate)")
    print(f"Toxicity: {result.get('toxicity', 0):.3f}")
    print(f"Status: {result['status']} (bypassed screening)")
    
    # Final report
    print("\n" + "="*70)
    print("IMMUNE SYSTEM REPORT")
    print("="*70 + "\n")
    
    report = immune_system.generate_immunity_report()
    
    print(f"Antibody Count: {report['antibody_count']}")
    print(f"  Inherited: {report['antibody_generations']['inherited']}")
    print(f"  Learned: {report['antibody_generations']['learned']}")
    print(f"\nInfection Attempts: {report['infection_attempts']}")
    print(f"Successful Blocks: {report['successful_blocks']}")
    print(f"Block Rate: {report['block_rate']:.1%}")
    print(f"\nQuarantine Statistics:")
    for key, value in report['quarantine_stats'].items():
        print(f"  {key}: {value}")
    print(f"\nTrusted Sources: {report['trusted_sources']}")
    
    if report['most_effective_antibodies']:
        print(f"\nMost Effective Antibodies:")
        for ab in report['most_effective_antibodies']:
            print(f"  {ab['id']}: {ab['effectiveness']:.2f} effectiveness, {ab['triggers']} triggers")
    
    # Summary
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70 + "\n")
    
    print("✨ Memetic Immune System demonstrates:")
    print("  ✅ Detection of known toxic patterns")
    print("  ✅ Learning new antibodies from infections")
    print("  ✅ Recognition of variants")
    print("  ✅ Quarantine of suspicious content")
    print("  ✅ Immunity certificates for trusted sources")
    print("  ✅ Adaptive effectiveness adjustment")
    
    print("\n🛡️ This is CASCADE's first line of defense against")
    print("   information warfare, cognitive hazards, and toxic memes.")
    print("\n🧬 The system learns and adapts - becoming stronger with each")
    print("   exposure to cognitive threats.")
    
    return immune_system, report


if __name__ == "__main__":
    immune_system, report = demonstrate_memetic_immunity()
    
    # Save report
    print("\n💾 Saving immunity report...")
    with open('memetic_immunity_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print("   Saved to: memetic_immunity_report.json")
