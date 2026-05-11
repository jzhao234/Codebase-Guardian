from agent_core.agent_state import create_initial_state
from agent_core.agent_planner import choose_next_action
from agent_core.agent_tools import run_action
from agent_core.agent_trace import add_trace


MAX_STEPS = 10


def run_agent_loop(repo_path, apply_fix=False):
    state = create_initial_state(repo_path, apply_fix)

    for _ in range(MAX_STEPS):
        if state["done"]:
            break

        next_action = choose_next_action(state)

        add_trace(
            state,
            "choose_next_action",
            next_action["reason"]
        )

        run_action(state, next_action)

    if not state["done"]:
        state["done"] = True
        state["final_status"] = "Stopped because max steps was reached."

        add_trace(
            state,
            "finish",
            "Stopped because max steps was reached."
        )

    return state