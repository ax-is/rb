import os

def get_env_variable(key):
    value = os.getenv(key)
    if value is None:
        raise Exception(f"Missing required environment variable: {key}")
    return value 