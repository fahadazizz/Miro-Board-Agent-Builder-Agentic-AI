# Agent System: RAGSystem
**Role:** Orchestrator
**Goal:** To orchestrate the interaction between all agents and ensure smooth execution of tasks in a Retrieval-Augmented Generation system.
**Type:** orchestrator

## Sub-Agents
### Main Agent
- **Role:** Central coordinator
- **Goal:** To orchestrate the interaction between all other agents and ensure smooth execution of tasks.
- **Description:** Acts as the primary agent that manages and coordinates the overall workflow of the RAG system.

### Query Augmentor
- **Role:** Query enhancement
- **Goal:** Improve query understanding and efficiency by applying augmentation methods.
- **Description:** Enhances user queries using different query analysis techniques for efficient processing.

### Task Orchestrator
- **Role:** Task decomposition
- **Goal:** Ensure optimal task distribution and execution for best response generation.
- **Description:** Breaks down user queries into smaller, manageable tasks for efficient handling.

### Retrieval Planner
- **Role:** Planning retrieval tasks
- **Goal:** Create effective plans to guide the information retrieval process.
- **Description:** Generates a perfect plan for each task related to information retrieval.

### Information Retriever
- **Role:** Data gathering
- **Goal:** Collect relevant data efficiently according to the generated plan.
- **Description:** Uses various tools to gather information based on the planned retrieval strategy.

### LLM Generator
- **Role:** Response generation
- **Goal:** Produce accurate and contextually appropriate answers to user queries.
- **Description:** Generates responses using a large language model based on retrieved information.

### Response Evaluator
- **Role:** Response assessment
- **Goal:** Ensure that the generated responses meet the required standards and accuracy.
- **Description:** Evaluates the quality of LLM-generated responses based on specific tasks.

### Response Refiner
- **Role:** Response improvement
- **Goal:** Enhance the clarity, coherence, and relevance of the output.
- **Description:** Refines and polishes the final response before delivering it to the user.

### Response Gatherer
- **Role:** Data aggregation
- **Goal:** Compile step-wise responses stored in the database into a unified output.
- **Description:** Gathers all partial responses from the database to form a complete answer.

## Tools
- **Query Analyzer**: Applies various techniques to analyze and understand user queries more effectively.
- **Task Decomposer**: Breaks complex user queries into simpler, actionable tasks.
- **Retrieval Strategy Planner**: Develops detailed plans for retrieving information based on individual tasks.
- **Multi-tool Information Retriever**: Utilizes different tools to collect information as per the planned retrieval strategy.
- **LLM Response Generator**: Generates natural language responses using a large language model.
- **Response Evaluator**: Assesses the relevance and correctness of generated responses against the original task.
- **Response Aggregator**: Collects and integrates partial responses stored in the database.

## Workflows
### MainWorkflow
_End-to-end workflow for processing user queries through a RAG system with multiple specialized agents and tools._

**Steps:**
1. **[Main Agent]** Receive and analyze the user query for RAG processing
2. **[Query Augmentor]** Enhance the user query using different query analysis techniques (Tools: Query Analyzer)
3. **[Task Orchestrator]** Break down the enhanced query into manageable tasks (Tools: Task Decomposer)
4. **[System]** Store pending tasks in temporary database
5. **[Retrieval Planner]** Generate a perfect retrieval plan for each task (Tools: Retrieval Strategy Planner)
6. **[Information Retriever]** Gather information using different tools based on the retrieval plan (Tools: Multi-tool Information Retriever)
7. **[System]** Store step-wise responses in database based on plan and task
8. **[Response Gatherer]** Gather all partial responses from database (Tools: Response Aggregator)
9. **[LLM Generator]** Generate response using LLM based on retrieved information (Tools: LLM Response Generator)
10. **[Response Evaluator]** Evaluate LLM-generated response based on the original task (Tools: Response Evaluator)
11. **[Response Refiner]** Refine and polish the final response
12. **[Main Agent]** Deliver the final response to the user
