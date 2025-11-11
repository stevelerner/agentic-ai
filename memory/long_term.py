"""Long-term memory with vector-based retrieval (simplified)."""
from typing import List, Dict, Any
import json
from pathlib import Path


class LongTermMemory:
    """
    Simplified long-term memory storage.
    In production, this would use a vector database like ChromaDB.
    """
    
    def __init__(self, storage_path: str = "/app/memory_store.json"):
        self.storage_path = Path(storage_path)
        self.memories: List[Dict[str, Any]] = []
        self._load()
    
    def _load(self):
        """Load memories from disk."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    self.memories = json.load(f)
            except Exception:
                self.memories = []
    
    def _save(self):
        """Save memories to disk."""
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump(self.memories, f, indent=2)
        except Exception as e:
            print(f"Failed to save memories: {e}")
    
    def store(self, content: str, metadata: Dict[str, Any] = None):
        """Store a memory."""
        memory = {
            "content": content,
            "metadata": metadata or {},
            "id": len(self.memories)
        }
        self.memories.append(memory)
        self._save()
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant memories.
        In production, this would use embeddings and vector similarity.
        For now, simple keyword matching.
        """
        query_lower = query.lower()
        scored_memories = []
        
        for memory in self.memories:
            content_lower = memory["content"].lower()
            # Simple relevance score based on keyword overlap
            score = sum(1 for word in query_lower.split() if word in content_lower)
            if score > 0:
                scored_memories.append((score, memory))
        
        # Sort by score and return top_k
        scored_memories.sort(reverse=True, key=lambda x: x[0])
        return [mem for score, mem in scored_memories[:top_k]]
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all memories."""
        return self.memories.copy()
    
    def clear(self):
        """Clear all memories."""
        self.memories = []
        self._save()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        return {
            "total_memories": len(self.memories),
            "storage_path": str(self.storage_path)
        }

