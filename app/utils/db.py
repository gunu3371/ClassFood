from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url="sqlite://./database.sqlite3",
        modules={"models": ["app.utils.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
