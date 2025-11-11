"""FastAPI backend for orchestrating agents."""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
import json
from datetime import datetime
import uuid

from agents.orchestrator import Orchestrator
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory

app = FastAPI(title="Agentic AI System", version="1.0.0")

# CORS middleware for web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
orchestrator = Orchestrator()
short_term_memory = ShortTermMemory()
long_term_memory = LongTermMemory()

# Task storage
tasks: Dict[str, Dict[str, Any]] = {}

# WebSocket connections
active_connections: List[WebSocket] = []


class TaskRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None


class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str


@app.get("/")
async def root():
    return {
        "service": "Agentic AI System",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/task", response_model=TaskResponse)
async def create_task(request: TaskRequest):
    """Create a new task for the agent system."""
    task_id = str(uuid.uuid4())
    
    tasks[task_id] = {
        "id": task_id,
        "query": request.query,
        "context": request.context,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
        "result": None
    }
    
    # Process task asynchronously
    asyncio.create_task(process_task(task_id))
    
    return TaskResponse(
        task_id=task_id,
        status="pending",
        message="Task created and queued for processing"
    )


async def process_task(task_id: str):
    """Process a task asynchronously."""
    task = tasks.get(task_id)
    if not task:
        return
    
    try:
        task["status"] = "processing"
        await broadcast_task_update(task_id, "processing")
        
        # Process with orchestrator
        result = orchestrator.process_task(
            task["query"],
            task.get("context")
        )
        
        task["status"] = "completed"
        task["result"] = result
        task["completed_at"] = datetime.utcnow().isoformat()
        
        # Store in long-term memory
        long_term_memory.store(
            f"Task: {task['query']}\nResult: {result.get('final_output', '')}",
            {"task_id": task_id, "timestamp": task["completed_at"]}
        )
        
        await broadcast_task_update(task_id, "completed")
        
    except Exception as e:
        task["status"] = "failed"
        task["error"] = str(e)
        await broadcast_task_update(task_id, "failed")


@app.get("/api/task/{task_id}")
async def get_task(task_id: str):
    """Get task status and details."""
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/api/tasks")
async def list_tasks(limit: int = 10):
    """List recent tasks."""
    task_list = sorted(
        tasks.values(),
        key=lambda x: x["created_at"],
        reverse=True
    )
    return task_list[:limit]


@app.get("/api/memory/short-term")
async def get_short_term_memory():
    """Get short-term conversation memory."""
    return {
        "messages": short_term_memory.get_messages(),
        "metadata": short_term_memory.metadata
    }


@app.get("/api/memory/long-term")
async def get_long_term_memory():
    """Get long-term memory statistics."""
    return long_term_memory.get_stats()


@app.post("/api/memory/long-term/query")
async def query_long_term_memory(query: str, top_k: int = 5):
    """Query long-term memory."""
    results = long_term_memory.retrieve(query, top_k)
    return {"query": query, "results": results}


@app.get("/api/agents/status")
async def get_agents_status():
    """Get status of all agents."""
    return {
        "orchestrator": "active",
        "agents": {
            "planner": "ready",
            "researcher": "ready",
            "analyst": "ready",
            "writer": "ready",
            "coder": "ready"
        }
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            # Echo back for now
            await websocket.send_text(f"Received: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)


async def broadcast_task_update(task_id: str, status: str):
    """Broadcast task update to all connected WebSocket clients."""
    message = json.dumps({
        "type": "task_update",
        "task_id": task_id,
        "status": status,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except:
            pass


@app.delete("/api/tasks/clear")
async def clear_tasks():
    """Clear all completed tasks."""
    global tasks
    tasks = {
        tid: task for tid, task in tasks.items()
        if task["status"] not in ["completed", "failed"]
    }
    return {"message": "Completed tasks cleared"}


@app.post("/api/orchestrator/reset")
async def reset_orchestrator():
    """Reset the orchestrator state."""
    orchestrator.reset()
    return {"message": "Orchestrator reset"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

