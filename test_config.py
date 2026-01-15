from app.core.config import settings
print("✅ Config loaded successfully!")
print(f"App: {settings.app_name}")
print(f"LM Studio: {settings.lm_studio_model}")
print(f"DB: {settings.database_url}")