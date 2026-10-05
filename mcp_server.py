"""MCP server for Episodic Agent Memory Indexer."""
import sys
import json
from client import EpisodicAgentMemoryManager

_manager = EpisodicAgentMemoryManager()

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "store_episodic_memory",
                    "description": "Stores a new episodic memory item with importance rating",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "tags": {"type": "array", "items": {"type": "string"}},
                            "importance": {"type": "number"}
                        },
                        "required": ["content", "tags"]
                    }
                },
                {
                    "name": "query_episodic_memories",
                    "description": "Retrieves memories matching a tag, ranked by time-decay score",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "tag": {"type": "string"}
                        },
                        "required": ["tag"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "store_episodic_memory":
            _manager.add_memory(args.get("content", ""), args.get("tags", []), args.get("importance", 1.0))
            return {"content": [{"type": "text", "text": json.dumps({"status": "stored", "total": len(_manager.memories)})}]}
        elif tool_name == "query_episodic_memories":
            res = _manager.query_memories(args.get("tag", ""))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
