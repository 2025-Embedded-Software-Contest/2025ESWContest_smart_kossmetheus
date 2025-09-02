import os


def ssl_available() -> bool:
    if os.getenv("SIMULATE_NO_SSL") == "1":
        return False
    
    try:
        import ssl # noqa: F401
        return True
    except ModuleNotFoundError:
        return False