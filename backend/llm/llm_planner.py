import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


ALLOWED_ACTIONS = {
    "run_analysis",
    "select_finding",
    "gather_context",
    "generate_suggestion",
    "run_fix_agent",
    "finish",
}


def summarize_state_for_planner(state):
    return {
        "goal": state.get("goal"),
        "apply_fix": state.get("apply_fix"),
        "has_analysis": state.get("analysis") is not None,
        "finding_count": len(state.get("findings", [])),
        "has_selected_finding": state.get("selected_finding") is not None,
        "has_selected_context": state.get("selected_context") is not None,
        "has_suggestion": state.get("suggestion") is not None,
        "has_fix_result": state.get("fix_result") is not None,
        "done": state.get("done"),
        "recent_trace": state.get("agent_trace", [])[-6:],
    }


def get_rule_safe_actions(state):
    safe_actions = []

    if state.get("analysis") is None:
        safe_actions.append("run_analysis")

    if state.get("analysis") is not None and state.get("findings") and state.get("selected_finding") is None:
        safe_actions.append("select_finding")

    if state.get("selected_finding") is not None and state.get("selected_context") is None:
        safe_actions.append("gather_context")

    if state.get("selected_context") is not None and state.get("suggestion") is None:
        safe_actions.append("generate_suggestion")

    if state.get("suggestion") is not None and state.get("apply_fix") and state.get("fix_result") is None:
        safe_actions.append("run_fix_agent")

    safe_actions.append("finish")

    return safe_actions


def choose_next_action_with_llm(state):
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")

    if not api_key:
        return {
            "action": None,
            "reason": "OPENAI_API_KEY is not set.",
            "error": True,
        }

    if not model:
        return {
            "action": None,
            "reason": "OPENAI_MODEL is not set.",
            "error": True,
        }

    client = OpenAI(api_key=api_key)

    safe_actions = get_rule_safe_actions(state)

    planner_prompt = {
        "task": "Choose the next action for a repo maintenance agent.",
        "rules": [
            "Return only valid JSON.",
            "Choose exactly one action from safe_actions.",
            "Do not invent new actions.",
            "Do not skip required prerequisite steps.",
            "If no useful action remains, choose finish.",
            "The Python system will execute the action. You only choose the next action."
        ],
        "state_summary": summarize_state_for_planner(state),
        "safe_actions": safe_actions,
        "response_shape": {
            "action": "one of safe_actions",
            "reason": "short explanation"
        }
    }

    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "You are a cautious planning agent for a codebase maintenance system. You choose the next safe action based on state."
            },
            {
                "role": "user",
                "content": json.dumps(planner_prompt)
            }
        ]
    )

    try:
        planner_decision = json.loads(response.output_text)
    except json.JSONDecodeError:
        return {
            "action": None,
            "reason": "LLM planner did not return valid JSON.",
            "raw_output": response.output_text,
            "error": True,
        }

    action = planner_decision.get("action")
    reason = planner_decision.get("reason", "No reason provided.")

    if action not in ALLOWED_ACTIONS:
        return {
            "action": None,
            "reason": f"LLM planner returned invalid action: {action}",
            "error": True,
        }

    if action not in safe_actions:
        return {
            "action": None,
            "reason": f"LLM planner chose an unsafe action for current state: {action}",
            "error": True,
        }

    return {
        "action": action,
        "reason": reason,
        "used_llm_planner": True,
    }