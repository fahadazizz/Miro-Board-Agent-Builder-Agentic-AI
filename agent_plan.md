# Agent System: Task Planning System
**Role:** Orchestrator
**Goal:** To efficiently plan and execute user tasks by researching relevant information, evaluating its relevance, and generating a comprehensive step-by-step plan.
**Type:** orchestrator

## Sub-Agents
### Research Agent
- **Role:** Information Gatherer
- **Goal:** Retrieve accurate and up-to-date data to support effective task planning.
- **Description:** Fetches updated and relevant information related to the user's task query, including code, documents, or other resources that aid in the planning process.

### Evaluator Agent
- **Role:** Quality Assurance
- **Goal:** Ensure the quality and relevance of the gathered information before proceeding to the planning stage.
- **Description:** Compares the researched data with the user's task query to ensure it meets the required standards. If not, the Evaluator signals the Research Agent to try again.

### Planning Agent
- **Role:** Task Strategist
- **Goal:** Create a comprehensive and actionable plan based on the evaluated research data.
- **Description:** Reasons through the user's task query and the researched data to devise the most efficient and complete approach. Generates a detailed, step-by-step plan for task execution.

## Tools
- **search_web**: Used by the Research Agent to find relevant online resources and information.
- **read_file**: Allows the Research Agent to access and extract data from documents or code files.
- **compare_data**: Enables the Evaluator Agent to assess the relevance and accuracy of the researched information against the user's task query.
- **generate_plan**: Assists the Planning Agent in creating a structured and efficient step-by-step plan for task execution.

## Workflows
### Task Planning Workflow
_A complete workflow that starts with receiving a user task query, followed by researching, evaluating, and finally planning the task._

**Steps:**
1. **[System]** Receive the user's task query and initiate the system prompts for each agent.
2. **[Research Agent]** Research Agent fetches relevant information based on the user's task query. (Tools: search_web, read_file)
3. **[Evaluator Agent]** Evaluator Agent compares the researched data with the user's task query to check for relevance and completeness. (Tools: compare_data)
4. **[Evaluator Agent]** If the data is insufficient, the Evaluator signals the Research Agent to re-research; otherwise, proceed to planning.
5. **[Planning Agent]** Planning Agent uses the validated data to generate a comprehensive and efficient step-by-step plan for the user's task. (Tools: generate_plan)
6. **[System]** Output the final plan to the user.
