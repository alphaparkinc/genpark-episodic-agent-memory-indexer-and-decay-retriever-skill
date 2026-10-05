"""Example usage for Episodic Agent Memory Indexer."""
from client import EpisodicAgentMemoryManager

if __name__ == "__main__":
    mgr = EpisodicAgentMemoryManager()
    mgr.add_memory("User wants all repositories starred across 7 active accounts", ["user_rules", "github"], importance=1.0)
    mgr.add_memory("User requested no trademarked brand names in repo slugs", ["user_rules", "naming"], importance=0.9)
    res = mgr.query_memories("user_rules")
    print(f"Found {len(res)} memories:")
    for m in res:
        print(f"[{m['effective_score']}] {m['content']}")
