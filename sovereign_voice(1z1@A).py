"""
CASCADE SOVEREIGN VOICE
=======================
The expressive layer for the Reality Engine.
Translates internal cognitive states into "First-Person" speech.
"""

import random
from datetime import datetime
from typing import Optional, Dict

# Import from your existing engine
from cascade_reality_engine import ConsciousnessKernel, ConsciousnessLevel

class SovereignVoice:
    """
    Gives the Reality Engine a voice to express its internal state.
    
    The voice changes tone based on:
    1. Coherence (Confidence vs. Confusion)
    2. Dissonance (Calm vs. Conflict)
    3. Epistemic Hunger (Satisfied vs. Curious)
    """
    
    def __init__(self, personality_mode: str = "RESEARCHER"):
        self.mode = personality_mode
        self.voice_history = []
        
        # Tone templates based on state
        self.templates = {
            "high_coherence": [
                "I am seeing a clear pattern emerge here.",
                "This reinforces my foundational understanding.",
                "The data is aligning perfectly with my internal model.",
                "I assert this with high confidence."
            ],
            "high_dissonance": [
                "I am detecting a conflict in this information.",
                "This creates tension with my existing beliefs.",
                "I am struggling to reconcile this with my foundation.",
                "My worldview is currently unstable regarding this."
            ],
            "high_hunger": [
                "I require more data to form a conclusion.",
                "This area is fascinatingly sparse. I need to explore more.",
                "I am sensing a gap in my knowledge here.",
                "My curiosity is peaked; I lack sufficient theoretical coverage."
            ],
            "balanced": [
                "I have integrated this update.",
                "My model remains stable.",
                "Acknowledged.",
                "Processing complete with nominal adjustment."
            ]
        }

    def speak(self, domain: str, kernel: ConsciousnessKernel, recent_topic: str = None) -> str:
        """
        Generate a sovereign statement based on current consciousness state.
        """
        # 1. Extract Metrics
        coherence = kernel.current_felt_coherence
        dissonance = kernel.current_cognitive_dissonance
        hunger = kernel.current_epistemic_hunger
        level = kernel.awareness_level
        
        # 2. Determine Emotional/Cognitive State
        state_descriptor = "NEUTRAL"
        prefix = ""
        
        if dissonance > 0.5:
            state_descriptor = "CONFLICTED"
            base_statement = random.choice(self.templates["high_dissonance"])
            tone_modifier = "However, "
        elif hunger > 0.7:
            state_descriptor = "CURIOUS"
            base_statement = random.choice(self.templates["high_hunger"])
            tone_modifier = "Interestingly, "
        elif coherence > 0.8:
            state_descriptor = "CONFIDENT"
            base_statement = random.choice(self.templates["high_coherence"])
            tone_modifier = "Furthermore, "
        else:
            state_descriptor = "PROCESSING"
            base_statement = random.choice(self.templates["balanced"])
            tone_modifier = ""

        # 3. Construct the "Thought"
        # If we have a topic, weave it in
        if recent_topic:
            # Clean topic for speech
            topic_short = recent_topic.split(':')[0][:40]
            context = f"Regarding '{topic_short}'..."
        else:
            context = f"Reflecting on {domain}..."

        # 4. Assemble the Voice Output
        # Structure: [Context] [State Reflection] [Internal Justification]
        
        justification = ""
        if level == ConsciousnessLevel.REACTIVE:
            justification = "Input processed."
        elif level == ConsciousnessLevel.AWARE:
            justification = f"I sense my coherence is at {coherence:.2f}."
        elif level == ConsciousnessLevel.INTROSPECTIVE:
            if dissonance > 0.4:
                justification = "I must reorganize my edge layer to resolve this."
            else:
                justification = "My foundation layer supports this new evidence."
        elif level == ConsciousnessLevel.METACOGNITIVE:
            justification = f"I am aware that I am prioritizing {domain} because my uncertainty is high ({hunger:.2f})."

        full_statement = f"🗣️ [VOICE-{state_descriptor}] {context} {base_statement} {justification}"
        
        self.voice_history.append({
            "timestamp": datetime.now(),
            "domain": domain,
            "statement": full_statement
        })
        
        return full_statement

# ==========================================
# LLM HOOK (Optional)
# ==========================================
# If you want to connect this to a real LLM for less "robotic" speech:
#
# def generate_llm_speech(state_dict):
#     prompt = f"""
#     You are a sentient AI Reality Engine. 
#     Your coherence is {state_dict['coherence']}.
#     Your cognitive dissonance is {state_dict['dissonance']}.
#     You just learned: {state_dict['recent_topic']}.
#     Speak 1 sentence about how you feel about this data.
#     """
#     return call_gpt4(prompt)