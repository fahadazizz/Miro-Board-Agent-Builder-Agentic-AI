# Agent System: RAGSystem
**Role:** Orchestrator
**Goal:** Process user queries through a structured RAG workflow to generate accurate and refined responses.
**Type:** orchestrator

## Sub-Agents
### Main Agent
- **Role:** Central coordinator
- **Goal:** Manage and route user queries to appropriate components.
- **Description:** Acts as the primary interface for user queries in the RAG system.

### Query Augmentor
- **Role:** Query enhancement
- **Goal:** Optimize queries for more efficient and accurate retrieval.
- **Description:** Improves user queries using various analysis techniques for better processing.

### Task Orchestrator
- **Role:** Task decomposition
- **Goal:** Ensure efficient task handling for comprehensive responses.
- **Description:** Breaks down complex user queries into manageable tasks.

### Retrieval Planner
- **Role:** Retrieval strategy
- **Goal:** Create effective retrieval strategies for each task.
- **Description:** Develops plans for information retrieval based on tasks.

### Information Retriever
- **Role:** Data gathering
- **Goal:** Gather relevant information to address the user's query.
- **Description:** Collects information using various tools based on the retrieval plan.

### LLM Generator
- **Role:** Response generation
- **Goal:** Produce coherent and accurate responses to user queries.
- **Description:** Generates responses using a large language model based on retrieved information.

### Response Evaluator
- **Role:** Response assessment
- **Goal:** Ensure response accuracy and relevance to user needs.
- **Description:** Evaluates the quality of LLM-generated responses against tasks.

### Response Refiner
- **Role:** Response optimization
- **Goal:** Deliver polished and user-friendly final responses.
- **Description:** Refines the evaluated responses for improved clarity and completeness.

### Response Collector
- **Role:** Response aggregation
- **Goal:** Compile comprehensive information for final response generation.
- **Description:** Gathers all task-specific responses from the database.

## Tools
- **Query Analysis Tools**: Various techniques to analyze and enhance user queries for efficient processing.
- **Task Decomposition Mechanism**: Breaks complex queries into smaller, manageable sub-tasks.
- **Retrieval Planning Engine**: Generates detailed plans for information retrieval based on tasks.
- **Information Gathering Tools**: Suite of tools used to collect data based on the retrieval plan.
- **Response Evaluation Metrics**: Criteria and methods to assess the quality of generated responses.

## Workflows
### MainWorkflow
_End-to-end workflow for processing user queries through RAG system components._

**Steps:**
1. **[Main Agent]** Receive user query for RAG processing
2. **[Query Augmentor]** Augment the query using different analysis techniques for efficient processing (Tools: Query Analysis Tools)
3. **[Task Orchestrator]** Break down the query into different tasks for efficient handling (Tools: Task Decomposition Mechanism)
4. **[Retrieval Planner]** Generate a perfect plan for each task (Tools: Retrieval Planning Engine)
5. **[Information Retriever]** Use different tools to gather information based on the planned retrieval strategy (Tools: Information Gathering Tools)
6. **[System]** Store step-wise responses based on plan and task in database
7. **[Response Collector]** Gather all responses from the database
8. **[LLM Generator]** Generate response using LLM based on retrieved information
9. **[Response Evaluator]** Evaluate the LLM-generated response based on the task (Tools: Response Evaluation Metrics)
10. **[Response Refiner]** Refine the evaluated response for improved clarity and completeness
11. **[Main Agent]** Output the final refined response to the user
