def choose_next_action(state):
    if state["analysis"] is None:
        return {
            "action": "run_analysis",
            "reason": "The repository has not been analyzed yet."
        }

    if not state["findings"]:
        return {
            "action": "finish",
            "reason": "No findings were detected."
        }

    if state["selected_finding"] is None:
        return {
            "action": "select_finding",
            "reason": "Findings exist, so the agent should select one to handle first."
        }

    if state["selected_context"] is None:
        return {
            "action": "gather_context",
            "reason": "The selected finding needs context before a fix can be suggested."
        }

    if state["suggestion"] is None:
        return {
            "action": "generate_suggestion",
            "reason": "Context is available, so the agent can generate a suggested fix."
        }

    if not state["apply_fix"]:
        return {
            "action": "finish",
            "reason": "A suggestion was generated, but apply_fix is disabled."
        }

    if state["fix_result"] is None:
        return {
            "action": "run_fix_agent",
            "reason": "apply_fix is enabled, so the Fix Agent should safely apply and verify the fix."
        }

    return {
        "action": "finish",
        "reason": "The agent has completed the available workflow."
    }