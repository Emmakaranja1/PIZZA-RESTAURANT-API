"""
Contains database configuration
"""

import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Emma2025@localhost:5432/pizza_api_db")