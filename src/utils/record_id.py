def generate_id() -> str:
    """
    Generate a unique 6-character alphanumeric ID.
    :return: A string representing the unique ID.
    """
    import random
    import string

    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))