def add_trace(state, action, reason, metadata=None):
    trace_entry = {
        "step": len(state["agent_trace"]) + 1,
        "action": action,
        "reason": reason,
    }

    if metadata is not None:
        trace_entry["metadata"] = metadata

    state["agent_trace"].append(trace_entry)