from decouple import config

class Settings:
    RECAPTCHA_SECRET_KEY = config("RECAPTCHA_SECRET_KEY")

    MONGO_DB_URL = config("MONGO_DB_URL")
    DATABASE_NAME = config("DATABASE_NAME")

    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_PORT = config("EMAIL_PORT", cast=int)
    smtp_user = config("smtp_user")
    smtp_password = config("smtp_password")

settings = Settings()
