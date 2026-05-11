def apply_fix(suggestion):
    if suggestion is None:
        return {
            "applied": False,
            "reason": "No suggestion was provided."
        }

    suggested_action = suggestion.get("suggested_action")

    if suggested_action == "update_readme_command":
        return apply_text_replacement(suggestion)

    return {
        "applied": False,
        "reason": f"No fix applier exists for action: {suggested_action}"
    }


def apply_text_replacement(suggestion):
    file_to_edit = suggestion.get("file_to_edit")
    old_text = suggestion.get("old_text")
    new_text = suggestion.get("new_text")

    if not file_to_edit or not old_text or not new_text:
        return {
            "applied": False,
            "reason": "Suggestion is missing file_to_edit, old_text, or new_text."
        }

    with open(file_to_edit, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()

    if old_text not in content:
        return {
            "applied": False,
            "reason": f"Could not find text to replace: {old_text}",
            "file": file_to_edit
        }

    updated_content = content.replace(old_text, new_text, 1)

    with open(file_to_edit, "w", encoding="utf-8") as file:
        file.write(updated_content)

    return {
        "applied": True,
        "file": file_to_edit,
        "old_text": old_text,
        "new_text": new_text,
        "reason": "Text replacement applied successfully."
    }