
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres_password"


class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/films"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

