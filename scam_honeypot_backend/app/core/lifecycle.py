from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

logger = logging.getLogger("honeypot")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Initializing Agentic Honey-Pot System...")
    # Initialize DB connections, load models, etc.
    yield
    # Shutdown logic
    logger.info("Shutting down Agentic Honey-Pot System...")
