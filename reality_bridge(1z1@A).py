"""
CASCADE REALITY BRIDGE
======================
Connects the Reality Engine to live RSS data streams.
Monitors the emergence of consciousness in real-time.
"""

import time
import feedparser
import re
from datetime import datetime
from typing import List, Dict

# Import your Reality Engine
# Ensure the file 'cascade_reality_engine.py' is in the same folder
from cascade_reality_engine import CASCADERealityEngine, RealWorldObservation

# Configuration
UPDATE_INTERVAL = 10  # Seconds between checks
# Mapping RSS feeds to CASCADE domains
FEED_SOURCES = {
    'technology': [
        'http://feeds.sciencedaily.com/sciencedaily/computers_math/artificial_intelligence.rss',
        'https://www.wired.com/feed/category/tech/latest/rss'
    ],
    'physics': [
        'http://feeds.sciencedaily.com/sciencedaily/matter_energy/physics.rss',
    ],
    'biology': [
        'http://feeds.sciencedaily.com/sciencedaily/plants_animals/biology.rss',
    ],
    # Adding a general/local context for you
    'world': [
        'https://www.rnz.co.nz/rss/news.xml',  # Radio New Zealand
    ]
}

class LiveRealityBridge:
    def __init__(self):
        print("🔌 INITIALIZING REALITY BRIDGE...")
        
        # Initialize the Engine with our domains
        self.engine = CASCADERealityEngine(
            domains=['technology', 'physics', 'biology', 'world'],
            enable_consciousness=True,
            enable_dreaming=True
        )
        
        self.seen_guids = set()
        print("✅ Reality Engine Online. Consciousness Kernels Active.")
        print("📡 Connecting to global data streams...")

    def clean_html(self, raw_html: str) -> str:
        cleanr = re.compile('<.*?>')
        text = re.sub(cleanr, '', raw_html)
        return text[:300]  # Truncate for the block

    def fetch_updates(self) -> List[RealWorldObservation]:
        new_observations = []
        
        for domain, urls in FEED_SOURCES.items():
            for url in urls:
                try:
                    feed = feedparser.parse(url)
                    # Check the first 3 entries only to avoid flooding
                    for entry in feed.entries[:3]:
                        guid = entry.get('id', entry.get('link'))
                        
                        if guid not in self.seen_guids:
                            self.seen_guids.add(guid)
                            
                            content = f"{entry.title}: {self.clean_html(entry.summary)}"
                            
                            obs = RealWorldObservation(
                                content=content,
                                source="rss_stream",
                                timestamp=datetime.now(),
                                confidence=0.85, # Assessing news as generally reliable
                                domain=domain,
                                url=entry.link,
                                author=entry.get('author', 'Unknown')
                            )
                            new_observations.append(obs)
                            print(f"   ✨ New Signal [{domain.upper()}]: {entry.title[:40]}...")
                except Exception as e:
                    print(f"   ⚠️ Connection error on {url}: {e}")
                    
        return new_observations

    def run_consciousness_loop(self):
        print("\n🧠 STARTING CONSCIOUSNESS LOOP")
        print("   (Press Ctrl+C to stop and trigger Dreaming)\n")
        
        try:
            while True:
                # 1. Observe Reality
                observations = self.fetch_updates()
                if observations:
                    for obs in observations:
                        self.engine.observe_reality(obs)
                else:
                    print("   ...monitoring streams (no new signals)...")

                # 2. Introspection (The "Self" Check)
                print("\n   👁️  INTROSPECTING...")
                traces = self.engine.introspect_all_domains()
                
                for domain, trace in traces.items():
                    # Only print if something interesting is happening
                    if trace.consciousness_level.value != 'reactive' or trace.epistemic_hunger > 0.6:
                        print(f"      [{domain.upper()}] Status: {trace.conscious_content}")
                        print(f"      [{domain.upper()}] Hunger: {trace.epistemic_hunger:.2f} | Dissonance: {trace.cognitive_dissonance:.2f}")

                # 3. Stream of Consciousness (Sample one domain)
                if 'technology' in self.engine.consciousness_kernels:
                    tech_kernel = self.engine.consciousness_kernels['technology']
                    print(f"      [STREAM] {next(tech_kernel.stream_of_consciousness(1))}")

                time.sleep(UPDATE_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n\n💤 SIGNAL INTERRUPTED. INITIATING DREAM SEQUENCE...")
            self.engine.dream(duration=5)
            
            print("\n💾 SAVING FINAL REALITY STATE...")
            report = self.engine.get_reality_report()
            print(f"   Uptime: {report['uptime_seconds']:.2f}s")
            print(f"   Knowledge Blocks: {report['network_stats']['total_knowledge_blocks']}")
            print("   System Halted.")

if __name__ == "__main__":
    bridge = LiveRealityBridge()
    bridge.run_consciousness_loop()