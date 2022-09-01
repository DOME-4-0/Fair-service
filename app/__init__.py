"""
app init
"""
from fastapi import FastAPI

from app.routers import connector


def create_app():
    """
    Create the FastAPI app
    """
    app = FastAPI()
    app.include_router(connector.router)
    return app
