"""
Base class for all database models
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Models will import Base from here
# To register models, import them in main.py before creating tables
