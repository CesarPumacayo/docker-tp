import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = os.getenv("MYSQL_USER", "docker_user")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "docker_password")
DB_HOST = os.getenv("MYSQL_HOST", "mysql")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE", "docker_tp")

# Aiven (y la mayoría de los proveedores de MySQL en la nube) exigen SSL.
# En Render, seteá la variable de entorno MYSQL_SSL=true para activarlo.
# En local (docker-compose) se deja sin definir y no se usa SSL.
usar_ssl = os.getenv("MYSQL_SSL", "false").lower() == "true"

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

connect_args = {"ssl": {"ssl_mode": "REQUIRED"}} if usar_ssl else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)