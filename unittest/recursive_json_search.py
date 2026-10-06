"""Search nested JSON-like data for values associated with a key."""

from policy import POLICY


def json_search(key, input_object, role=None):
    """Return every value associated with key in nested dictionaries and lists.

    Fields listed in ``POLICY`` are returned only to roles authorized for that
    field. Unlisted fields remain searchable without a role.
    """
    allowed_roles = POLICY.get(key)
    if allowed_roles is not None and role not in allowed_roles:
        return []

    matches = []

    def search(value):
        if isinstance(value, dict):
            for current_key, current_value in value.items():
                if current_key == key:
                    matches.append(current_value)
                search(current_value)
        elif isinstance(value, list):
            for item in value:
                search(item)

    search(input_object)
    return matches
