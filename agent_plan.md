# Agent System: RAGOrchestrator
**Role:** Orchestrator
**Goal:** Ensure efficient processing and response generation for user queries using a specialized RAG architecture with multiple agents and tools.
**Type:** orchestrator

## Sub-Agents
### MainAgent
- **Role:** Coordinator
- **Goal:** Ensure efficient processing and response generation for user queries.
- **Description:** Central agent responsible for orchestrating the overall process and delegating tasks to other sub-agents.

### QueryAugmentor
- **Role:** Query Enhancer
- **Goal:** Improve query efficiency and accuracy by applying augmentation techniques.
- **Description:** Enhances user queries using different query analyzer techniques for better understanding and processing.

### TaskOrchestrator
- **Role:** Task Manager
- **Goal:** Decompose complex queries into manageable tasks for streamlined processing.
- **Description:** Breaks down user queries into smaller tasks for efficient and accurate response generation.

### RetrievalPlanner
- **Role:** Planning Agent
- **Goal:** Create optimized plans for executing each decomposed task effectively.
- **Description:** Generates a detailed plan for each task to guide the retrieval and processing steps.

### InformationRetriever
- **Role:** Data Collector
- **Goal:** Retrieve relevant data efficiently according to the task plan.
- **Description:** Gathers information using various tools based on the planned tasks.

### LLMGenerator
- **Role:** Response Generator
- **Goal:** Produce accurate and contextually relevant responses to user queries.
- **Description:** Generates responses using a large language model based on retrieved information.

### ResponseEvaluator
- **Role:** Quality Assurance
- **Goal:** Validate response accuracy and relevance before final output.
- **Description:** Evaluates the generated responses based on the original tasks to ensure quality.

### ResponseRefiner
- **Role:** Finalizer
- **Goal:** Polish and finalize the response for optimal user satisfaction.
- **Description:** Refines the evaluated responses by gathering all relevant data from the database.

## Tools
- **QueryAnalyzer**: Applies various techniques to analyze and enhance user queries for better processing.
- **TaskDecomposer**: Breaks complex user queries into smaller, manageable tasks.
- **PlanGenerator**: Creates a structured plan for executing each task efficiently.
- **InformationGatheringTools**: Uses various tools to collect relevant information based on the generated plan.
- **DatabaseStorage**: Stores step-wise responses and task-related data for retrieval and refinement.
- **TemporaryTaskStorage**: Holds pending tasks temporarily during processing.
- **ResponseEvaluatorTool**: Evaluates LLM-generated responses based on task requirements and quality benchmarks.

## Workflows
### MainWorkflow
_End-to-end workflow for processing user queries using RAG architecture with multiple specialized agents and tools._

**Steps:**
1. **[MainAgent]** Receive and analyze the user query for RAG processing
2. **[QueryAugmentor]** Augment the query using different query analyzer techniques for efficient working (Tools: QueryAnalyzer)
3. **[TaskOrchestrator]** Break the user query into different tasks for efficient and best response (Tools: TaskDecomposer)
4. **[System]** Store pending tasks in temporary database (Tools: TemporaryTaskStorage)
5. **[RetrievalPlanner]** Generate a perfect plan for each task (Tools: PlanGenerator)
6. **[InformationRetriever]** Use different tools to gather information based on the planned tasks (Tools: InformationGatheringTools)
7. **[System]** Store step-wise responses based on plan and task in database (Tools: DatabaseStorage)
8. **[LLMGenerator]** Generate response using LLM based on retrieved information
9. **[ResponseEvaluator]** Evaluate response of LLM generation based on the task (Tools: ResponseEvaluatorTool)
10. **[ResponseRefiner]** Gather all responses from database for refinement (Tools: DatabaseStorage)
11. **[ResponseRefiner]** Refine and finalize the response for optimal user satisfaction
12. **[MainAgent]** Output the final response to the user
