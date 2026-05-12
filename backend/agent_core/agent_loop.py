from agent_core.agent_state import create_initial_state
from agent_core.agent_planner import choose_next_action
from agent_core.agent_tools import run_action
from agent_core.agent_trace import add_trace


MAX_STEPS = 10


def run_agent_loop(repo_path, apply_fix=False, use_llm=False, use_llm_planner=False):
    state = create_initial_state(repo_path, apply_fix, use_llm, use_llm_planner=False)

    for _ in range(MAX_STEPS):
        if state["done"]:
            break

        next_action = choose_next_action(state)

        planner_action_name = "choose_next_action"

        if next_action.get("used_llm_planner"):
            planner_action_name = "choose_next_action_llm"

        add_trace(
            state,
            planner_action_name,
            next_action["reason"],
            metadata={
                "chosen_action": next_action["action"]
            }
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