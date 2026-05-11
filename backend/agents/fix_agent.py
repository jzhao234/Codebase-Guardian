import fix_applier
import diff_generator
import git_manager

from agents import verifier_agent


def run_fix_agent(repo_path, suggestion, selected_finding, run_analysis_pass):
    fix_state = {
        "branch": None,
        "fix_result": None,
        "diff": None,
        "verification": None,
        "commit": None,
    }

    branch_result = git_manager.create_fix_branch(repo_path)
    fix_state["branch"] = branch_result

    if not branch_result["success"]:
        fix_state["fix_result"] = {
            "applied": False,
            "reason": "Could not create fix branch.",
            "error": branch_result["error"],
        }
        return fix_state

    fix_result = fix_applier.apply_fix(suggestion)
    fix_state["fix_result"] = fix_result

    if not fix_result.get("applied"):
        fix_state["verification"] = {
            "reran_analysis": False,
            "reason": "Fix was not applied, so verification was skipped.",
        }
        return fix_state

    diff_result = diff_generator.generate_git_diff(repo_path)
    fix_state["diff"] = diff_result

    verification_result = verifier_agent.verify_fix(
        repo_path,
        selected_finding,
        run_analysis_pass
    )

    fix_state["verification"] = verification_result

    if verification_result["selected_finding_resolved"]:
        commit_result = git_manager.commit_changes(
            repo_path,
            "Apply agent-suggested maintenance fix"
        )

        fix_state["commit"] = commit_result
    else:
        fix_state["commit"] = {
            "success": False,
            "committed": False,
            "error": "Fix was applied, but the selected finding was not resolved. Commit skipped.",
        }

    return fix_state