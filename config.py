import os

app_env = os.getenv("APP_ENV", "development")

if app_env == "development":
    GPT_TYPE = "gpt-4o-mini"
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:3001"]
    BOT_LINK = "http://127.0.0.1:8001"
elif app_env == "prod":
    GPT_TYPE = "gpt-4o"
    CORS_ORIGINS = [""]
    BOT_LINK = ""
else:
    raise ValueError(f"Unknown environment: {app_env}")

DISABLE_REWIND = True