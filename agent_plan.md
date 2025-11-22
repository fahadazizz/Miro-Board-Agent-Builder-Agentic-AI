# Agent System: RAG Query Processing System
**Role:** Orchestrator
**Goal:** Process user queries using RAG to retrieve and generate accurate responses
**Type:** orchestrator

## Sub-Agents
### MainAgent
- **Role:** Coordinator
- **Goal:** Coordinate all sub-agents to process user query effectively
- **Description:** Central agent that manages the overall query processing flow

### QueryAugmentor
- **Role:** QueryProcessor
- **Goal:** Improve query quality using various analysis techniques
- **Description:** Enhances and refines user queries for better processing

### TaskOrchestrator
- **Role:** TaskManager
- **Goal:** Decompose complex queries into actionable tasks
- **Description:** Breaks down queries into manageable tasks

### RetrievalPlanner
- **Role:** PlanningAgent
- **Goal:** Generate effective retrieval strategies for each task
- **Description:** Creates retrieval plans for each task

### InformationRetriever
- **Role:** RetrievalAgent
- **Goal:** Retrieve relevant information using various tools
- **Description:** Gathers information based on retrieval plans

### LLMGenerator
- **Role:** ResponseGenerator
- **Goal:** Create accurate and comprehensive responses
- **Description:** Generates responses using retrieved information

### ResponseEvaluator
- **Role:** QualityAssurance
- **Goal:** Ensure responses meet quality standards
- **Description:** Evaluates the quality of generated responses

### ResponseRefiner
- **Role:** ResponseOptimizer
- **Goal:** Improve response clarity and accuracy
- **Description:** Refines and optimizes final responses

### ResponseGatherer
- **Role:** DataCollector
- **Goal:** Aggregate all relevant information for response generation
- **Description:** Collects responses from database for final processing

## Tools
- **query_analyzer**: Analyzes queries using different techniques for efficient processing
- **task_breaker**: Breaks user queries into different tasks for efficient handling
- **plan_generator**: Generates perfect plans for each task
- **information_gatherer**: Uses different tools to gather information based on planned strategies
- **response_evaluator**: Evaluates LLM-generated responses based on assigned tasks

## Workflows
### QueryProcessingWorkflow
_End-to-end workflow for processing user queries using RAG_

**Steps:**
1. **[MainAgent]** Receive and analyze user query for RAG processing
2. **[QueryAugmentor]** Augment and refine the query using advanced analysis techniques (Tools: query_analyzer)
3. **[TaskOrchestrator]** Break down the query into manageable tasks (Tools: task_breaker)
4. **[RetrievalPlanner]** Generate retrieval plans for each task (Tools: plan_generator)
5. **[InformationRetriever]** Retrieve information based on generated plans (Tools: information_gatherer)
6. **[System]** Store step-wise responses in database based on plans and tasks
7. **[ResponseGatherer]** Gather all responses from database for processing
8. **[LLMGenerator]** Generate final response using LLM
9. **[ResponseEvaluator]** Evaluate the quality of generated response (Tools: response_evaluator)
10. **[ResponseRefiner]** Refine and optimize the final response
11. **[MainAgent]** Deliver final response to user
