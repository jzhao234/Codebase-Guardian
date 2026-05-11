def create_initial_state(repo_path, apply_fix=False, use_llm=False):
    return {
        "goal": "Find and safely fix repo maintenance issues.",

        "use_llm": use_llm,

        "repo_path": repo_path,
        "apply_fix": apply_fix,

        "analysis": None,
        "repo_map": [],
        "findings": [],

        "selected_finding": None,
        "selected_context": None,
        "suggestion": None,

        "branch": None,
        "fix_result": None,
        "diff": None,
        "verification": None,
        "commit": None,

        "agent_trace": [],
        "done": False,
        "final_status": None,
    }