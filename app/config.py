
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres_password"


class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/films"

