import argparse
import json
import sys
import os

# Ensure src is in path if running from root
sys.path.append(os.path.join(os.getcwd(), "src"))

try:
    from agent import app
    from config import Config
except ImportError:
    from src.agent import app
    from src.config import Config

def main():
    parser = argparse.ArgumentParser(description="Miro Board to Agent DSL Converter")
    parser.add_argument("url", help="Miro Board URL")
    parser.add_argument("--output", "-o", help="Output file for DSL JSON", default="agent_plan.json")
    
    args = parser.parse_args()
    
    print(f"Starting Miro Agent for URL: {args.url}")
    Config.validate()
    
    # Set LangSmith Environment Variables
    if Config.LANGCHAIN_TRACING_V2:
        os.environ["LANGCHAIN_TRACING_V2"] = Config.LANGCHAIN_TRACING_V2
    if Config.LANGCHAIN_ENDPOINT:
        os.environ["LANGCHAIN_ENDPOINT"] = Config.LANGCHAIN_ENDPOINT
    if Config.LANGCHAIN_API_KEY:
        os.environ["LANGCHAIN_API_KEY"] = Config.LANGCHAIN_API_KEY
    if Config.LANGCHAIN_PROJECT:
        os.environ["LANGCHAIN_PROJECT"] = Config.LANGCHAIN_PROJECT
    
    initial_state = {"board_url": args.url}
    result = app.invoke(initial_state)
    
    if result.get("error"):
        print(f"Error: {result['error']}")
        sys.exit(1)
        
    dsl = result.get("agent_dsl")
    if dsl:
        print("\n--- Generated Agent DSL ---\n")
        print(json.dumps(dsl, indent=2))
        
        # Save JSON
        with open(args.output, "w") as f:
            json.dump(dsl, f, indent=2)
        print(f"\nJSON Plan saved to {args.output}")
        
        # Save Plain Text/Markdown
        text_output_file = args.output.rsplit('.', 1)[0] + ".md"
        text_plan = format_dsl_to_text(dsl)
        with open(text_output_file, "w") as f:
            f.write(text_plan)
        print(f"Text Plan saved to {text_output_file}")
        
        # Print Text Plan to console for immediate view
        print("\n--- Plain Text Plan ---\n")
        print(text_plan)
    else:
        print("Failed to generate DSL.")

def format_dsl_to_text(dsl: dict) -> str:
    lines = []
    lines.append(f"# Agent System: {dsl.get('name', 'Unnamed System')}")
    lines.append(f"**Role:** {dsl.get('role', 'N/A')}")
    lines.append(f"**Goal:** {dsl.get('goal', 'N/A')}")
    lines.append(f"**Type:** {dsl.get('type', 'orchestrator')}")
    lines.append("")
    
    if dsl.get('sub_agents'):
        lines.append("## Sub-Agents")
        for agent in dsl.get('sub_agents', []):
            lines.append(f"### {agent.get('name')}")
            lines.append(f"- **Role:** {agent.get('role')}")
            lines.append(f"- **Goal:** {agent.get('goal', 'N/A')}")
            lines.append(f"- **Description:** {agent.get('description')}")
            lines.append("")
    
    lines.append("## Tools")
    for tool in dsl.get('tools', []):
        lines.append(f"- **{tool.get('name')}**: {tool.get('description')}")
    lines.append("")
    
    lines.append("## Workflows")
    for wf in dsl.get('workflows', []):
        lines.append(f"### {wf.get('name')}")
        lines.append(f"_{wf.get('description')}_")
        lines.append("")
        lines.append("**Steps:**")
        for step in wf.get('steps', []):
            assigned = f"**[{step.get('assigned_to', 'System')}]** " if step.get('assigned_to') else ""
            tools = ", ".join(step.get('tools_required', []))
            tools_str = f" (Tools: {tools})" if tools else ""
            lines.append(f"{step.get('step_id')}. {assigned}{step.get('description')}{tools_str}")
        lines.append("")
        
    return "\n".join(lines)

if __name__ == "__main__":
    main()
