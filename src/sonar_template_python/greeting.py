def greet(name: str = "") -> str:
    """Return a greeting, falling back to "world" for a blank name."""
    cleaned = name.strip()
    return f"Hello, {cleaned or 'world'}!"
