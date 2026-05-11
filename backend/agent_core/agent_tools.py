from agents import resource_auditor_agent
import decision_engine
import context_gatherer
import suggestion_generator

from agent_core.agent_trace import add_trace
from agents import fix_agent


def run_action(state, action):
    action_name = action["action"]

    if action_name == "run_analysis":
        analysis = resource_auditor_agent.run_resource_audit(state["repo_path"])

        state["analysis"] = analysis
        state["repo_map"] = analysis["repo_map"]
        state["findings"] = analysis["findings"]

        add_trace(
            state,
            "run_analysis",
            f"Analyzed repository and found {len(state['findings'])} finding(s)."
        )
        return

    if action_name == "select_finding":
        decision = decision_engine.choose_next_action(state["findings"])

        if decision["action"] == "prioritize_finding":
            state["selected_finding"] = decision["selected_finding"]

            add_trace(
                state,
                "select_finding",
                f"Selected finding: {state['selected_finding']['type']}."
            )
        else:
            add_trace(
                state,
                "select_finding",
                "No finding was selected."
            )

        return

    if action_name == "gather_context":
        selected_context = context_gatherer.gather_context_for_finding(
            state["selected_finding"],
            state["analysis"]
        )

        state["selected_context"] = selected_context

        add_trace(
            state,
            "gather_context",
            "Gathered relevant context for the selected finding."
        )
        return

    if action_name == "generate_suggestion":
        suggestion = suggestion_generator.generate_suggestion(
            state["selected_context"]
        )

        state["suggestion"] = suggestion

        add_trace(
            state,
            "generate_suggestion",
            f"Generated suggestion: {suggestion.get('suggested_action')}."
        )
        return

    if action_name == "run_fix_agent":
        fix_state = fix_agent.run_fix_agent(
            state["repo_path"],
            state["suggestion"],
            state["selected_finding"],
            resource_auditor_agent.run_resource_audit
        )

        state["branch"] = fix_state["branch"]
        state["fix_result"] = fix_state["fix_result"]
        state["diff"] = fix_state["diff"]
        state["verification"] = fix_state["verification"]
        state["commit"] = fix_state["commit"]

        add_trace(
            state,
            "run_fix_agent",
            "Fix Agent finished applying, verifying, and optionally committing the fix."
        )
        return

    if action_name == "finish":
        state["done"] = True
        state["final_status"] = action["reason"]

        add_trace(
            state,
            "finish",
            action["reason"]
        )
        return

    state["done"] = True
    state["final_status"] = f"Unknown action: {action_name}"

    add_trace(
        state,
        "error",
        f"Unknown action: {action_name}"
    )