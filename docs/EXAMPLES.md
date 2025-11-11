# Example Use Cases

This document provides detailed examples of how to use the Agentic AI system for various tasks.

## Example 1: Research & Report Generation

### Task
Research a technical topic and generate a comprehensive report with sources.

### Query
```
Research the latest developments in AI agents and agentic AI systems.

Focus on:
1. Key concepts and terminology
2. Recent breakthroughs (2023-2024)
3. Practical applications
4. Future trends

Create a comprehensive report with sources.
```

### Expected Flow

1. **Planner** creates execution plan:
   - Step 1: Researcher searches for AI agent information
   - Step 2: Researcher searches for recent breakthroughs
   - Step 3: Analyst synthesizes findings
   - Step 4: Writer creates structured report
   - Step 5: Writer saves report to file

2. **Researcher** executes searches:
   ```
   Tool: web_search("AI agents 2024")
   Tool: web_search("agentic AI systems")
   Tool: web_search("AI agent frameworks")
   ```

3. **Analyst** processes results:
   - Identifies key trends
   - Categorizes findings
   - Highlights important sources

4. **Writer** creates report:
   - Structures information
   - Adds citations
   - Formats as markdown
   - Saves to `outputs/ai_agents_report.md`

### Try It

**Web UI:**
1. Navigate to http://localhost:8080
2. Paste the query above
3. Click Send
4. Watch agents collaborate in real-time

**CLI:**
```bash
make cli
# Then paste the query
```

**API:**
```bash
curl -X POST http://localhost:8000/api/task \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Research the latest developments in AI agents..."
  }'
```

### Expected Output

A markdown report with:
- Executive summary
- Key concepts explained
- Recent developments with dates
- Practical applications
- Source citations with URLs
- Future predictions

---

## Example 2: Comparative Analysis

### Task
Compare different technologies and provide recommendations.

### Query
```
Analyze the pros and cons of different database architectures for a high-traffic web application.

Compare:
- Relational databases (PostgreSQL, MySQL)
- NoSQL databases (MongoDB, Cassandra)
- NewSQL databases (CockroachDB)
- Cache layers (Redis, Memcached)

Consider:
- Performance and scalability
- Consistency guarantees
- Operational complexity
- Cost

Provide recommendations for different use cases.
```

### Expected Flow

1. **Planner**: Creates comparison framework
2. **Researcher**: Gathers information on each database type
3. **Analyst**: Compares features, creates pros/cons lists
4. **Analyst**: Identifies use cases for each
5. **Writer**: Creates comparative report with recommendations

### Output Structure

```markdown
# Database Architecture Analysis

## Executive Summary
[High-level findings]

## Detailed Comparison

### Relational Databases
**Pros:**
- [List]

**Cons:**
- [List]

### NoSQL Databases
[...]

## Recommendations

### Use Case 1: E-commerce Site
Recommendation: PostgreSQL + Redis
Rationale: [...]

### Use Case 2: Social Media Feed
Recommendation: Cassandra
Rationale: [...]
```

---

## Example 3: Code Generation

### Task
Generate production-quality code with tests.

### Query
```
Generate a production-ready Python REST API with the following features:

1. User authentication (JWT tokens)
2. CRUD operations for a 'tasks' resource
3. Input validation
4. Error handling
5. Basic unit tests
6. API documentation

Use FastAPI framework and include:
- Main application file
- Authentication module
- Data models
- API routes
- Tests
- README with setup instructions
```

### Expected Flow

1. **Planner**: Breaks down into components
2. **Researcher**: Finds FastAPI best practices
3. **Coder**: Generates authentication module
4. **Coder**: Generates data models
5. **Coder**: Generates API routes
6. **Coder**: Generates tests
7. **Coder**: Validates code (execute_code tool)
8. **Writer**: Creates README
9. **Writer**: Saves all files

### Output Files

```
outputs/
├── main.py           # FastAPI application
├── auth.py           # JWT authentication
├── models.py         # Pydantic models
├── routes.py         # API endpoints
├── test_api.py       # Unit tests
└── README.md         # Setup instructions
```

### Validation

The Coder agent can execute the tests to validate the code:

```python
Tool: execute_code(code="pytest test_api.py", language="python")
```

---

## Example 4: Explain-Simplify Task

### Task
Explain a complex topic in simple terms.

### Query
```
Explain quantum computing concepts and create a beginner-friendly guide.

Cover:
- What is quantum computing?
- How is it different from classical computing?
- Key concepts (qubits, superposition, entanglement)
- Current applications
- Future potential

Use analogies and examples. Make it accessible to someone with no physics background.
```

### Expected Flow

1. **Planner**: Creates educational structure
2. **Researcher**: Gathers quantum computing information
3. **Analyst**: Identifies key concepts to explain
4. **Writer**: Creates beginner-friendly guide with analogies
5. **Writer**: Saves to markdown

### Output Style

The Writer agent will create content like:

```markdown
# Quantum Computing: A Beginner's Guide

## What is Quantum Computing?

Imagine a regular computer as a light switch - it's either ON or OFF.
A quantum computer is like a dimmer switch - it can be in many states at once!

## Key Concepts

### Qubits
Think of a qubit like a coin spinning in the air. While it's spinning,
it's both heads AND tails at the same time...
```

---

## Example 5: Multi-Step Data Pipeline

### Task
Process data through multiple analysis steps.

### Query
```
I have sales data for Q4 2024. Analyze it and create a comprehensive report.

Steps:
1. Load and validate the data
2. Calculate key metrics (revenue, growth, trends)
3. Identify top-performing products
4. Create visualizations
5. Generate insights and recommendations
6. Format as executive report

Context: E-commerce company, 50K+ transactions
```

### Expected Flow

1. **Planner**: Creates data analysis pipeline
2. **Coder**: Generates data loading script
3. **Analyst**: Processes data, calculates metrics
4. **Analyst**: Identifies patterns and trends
5. **Coder**: Generates visualization code
6. **Writer**: Creates executive report
7. **Writer**: Saves report and visualizations

### Tools Used

- `analyze_data`: Process structured data
- `execute_code`: Run analysis scripts
- `create_summary`: Summarize findings
- `save_file`: Save outputs

---

## Example 6: Documentation Generation

### Task
Generate documentation for existing code.

### Query
```
Create comprehensive documentation for a Python project.

The project is a task management API. Generate:
1. API reference (endpoints, parameters, responses)
2. Getting started guide
3. Authentication guide
4. Example usage
5. Troubleshooting guide

Make it suitable for developers integrating with the API.
```

### Expected Flow

1. **Planner**: Creates documentation structure
2. **Coder**: Analyzes code structure
3. **Writer**: Creates API reference
4. **Writer**: Creates getting started guide
5. **Writer**: Creates examples
6. **Writer**: Saves all documentation

---

## Example 7: Problem-Solving Task

### Task
Debug and fix issues.

### Query
```
My Python script is running slowly. Help me identify and fix performance issues.

The script processes 100K records and takes 10 minutes.

Current approach:
- Loads all data into memory
- Loops through records one by one
- Makes database query for each record
- No caching

Provide optimizations and improved code.
```

### Expected Flow

1. **Planner**: Creates optimization strategy
2. **Analyst**: Identifies bottlenecks
3. **Coder**: Generates optimized version
4. **Coder**: Validates improvements
5. **Writer**: Documents changes and performance gains

### Expected Recommendations

- Batch database queries
- Use generators instead of lists
- Add caching layer
- Parallel processing
- Database indexing

---

## Example 8: Learning Task

### Task
Learn a new technology.

### Query
```
I want to learn Docker. Create a comprehensive learning plan.

Include:
- Core concepts
- Hands-on exercises (beginner to advanced)
- Best practices
- Common pitfalls
- Project ideas

Format as a 7-day learning path.
```

### Expected Flow

1. **Planner**: Creates learning curriculum
2. **Researcher**: Finds Docker resources
3. **Analyst**: Organizes by difficulty
4. **Writer**: Creates day-by-day plan
5. **Coder**: Generates exercise code
6. **Writer**: Saves comprehensive guide

---

## Tips for Effective Queries

### 1. Be Specific

❌ Bad: "Tell me about AI"
✅ Good: "Explain transformer architecture in neural networks, focusing on attention mechanisms"

### 2. Provide Context

❌ Bad: "Generate code"
✅ Good: "Generate Python code for a REST API using FastAPI with authentication"

### 3. Define Scope

❌ Bad: "Research databases"
✅ Good: "Compare PostgreSQL vs MongoDB for a social media app with 1M users"

### 4. Specify Output Format

❌ Bad: "Analyze this"
✅ Good: "Analyze this data and create a report with charts saved to PDF"

### 5. Break Complex Tasks

❌ Bad: "Build a complete e-commerce platform"
✅ Good: "Design the database schema for an e-commerce platform with users, products, and orders"

---

## Running Pre-Built Examples

### Method 1: Makefile

```bash
# Run all examples
make examples

# Run specific example
make example-research
make example-analysis
make example-coding
```

### Method 2: Direct Execution

```bash
docker compose exec orchestrator python -m examples.research_task
docker compose exec orchestrator python -m examples.analysis_task
docker compose exec orchestrator python -m examples.coding_task
```

### Method 3: Web UI

1. Open http://localhost:8080
2. Click an example button
3. Modify if desired
4. Send

---

## Customizing Examples

Edit example files in `examples/`:

```python
# examples/custom_task.py
from agents.orchestrator import Orchestrator

orchestrator = Orchestrator()

task = """Your custom task here"""

result = orchestrator.process_task(task)
print(result["final_output"])
```

Run:
```bash
docker compose exec orchestrator python examples/custom_task.py
```

---

## Monitoring Execution

### View Logs
```bash
make logs-orch
```

### Check Execution Details
- **Web UI**: Click "Execution Log" tab
- **API**: GET `/api/task/{task_id}`

### View Generated Files
```bash
ls -la outputs/
cat outputs/report.md
```

---

Experiment with these examples to understand how multi-agent systems collaborate on complex tasks!

