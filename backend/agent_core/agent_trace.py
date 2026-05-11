def add_trace(state, action, reason):
    state["agent_trace"].append({
        "step": len(state["agent_trace"]) + 1,
        "action": action,
        "reason": reason,
    })