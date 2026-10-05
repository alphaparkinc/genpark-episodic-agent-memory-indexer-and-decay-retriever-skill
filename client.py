"""Episodic Agent Memory Indexer & Decay Retriever.
100% Python Standard Library.
"""

import time
import math

class EpisodicAgentMemoryManager:
    """Stores agent episodic memories with semantic tag indexes and time-decay relevance calculation."""
    
    def __init__(self, decay_rate: float = 0.05):
        self.decay_rate = decay_rate
        self.memories = []
        
    def add_memory(self, content: str, tags: list, importance: float = 1.0):
        self.memories.append({
            "id": len(self.memories) + 1,
            "content": content,
            "tags": [t.lower() for t in tags],
            "importance": importance,
            "timestamp": time.time()
        })
        
    def query_memories(self, tag: str, current_time: float = None) -> list:
        now = current_time if current_time is not None else time.time()
        tag_lower = tag.lower()
        results = []
        
        for m in self.memories:
            if tag_lower in m["tags"]:
                age_hours = max(0.0, (now - m["timestamp"]) / 3600.0)
                effective_score = m["importance"] * math.exp(-self.decay_rate * age_hours)
                results.append({
                    "id": m["id"],
                    "content": m["content"],
                    "effective_score": round(effective_score, 4),
                    "age_hours": round(age_hours, 2)
                })
                
        results.sort(key=lambda x: x["effective_score"], reverse=True)
        return results
