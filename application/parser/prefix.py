from .. import exceptions

def validate(prefix: str):
    """
    Validate the prefix and auto-fix common issues.
    - checks for invalid characters
    - adds a dash if missing
    - returns all lowercase
    """
    if prefix == "*empty*":  # empty prefix is allowed explicitly
        return ""
    if prefix is None:
        raise exceptions.InvalidPrefix(f"Prefix {prefix} is not valid.")
    invalid_characters = ['"', "'", " ", "\t", "\r", "\n", "/", "\\", "*"]
    if any([c in invalid_characters for c in prefix]):
        raise exceptions.InvalidPrefix(f"Prefix {prefix} is not valid and may not contain {invalid_characters}.")
    if not prefix.endswith("-"):
        prefix = f"{prefix}-"
    return prefix.lower()
