from langchain_community.utilities.sql_database import SQLDatabase
from app.database.get_database import get_engine_for_chinook_db

def get_database():
    """
    Initialize and return the SQLDatabase instance for the Chinook database.
    
    This function creates a SQLAlchemy engine connected to an in-memory SQLite database
    populated with the Chinook sample data, and wraps it in a LangChain SQLDatabase object.
    
    Returns:
        SQLDatabase: A LangChain SQLDatabase instance for querying the Chinook database.
    """
    # Initialize the database engine with the Chinook sample data
    engine = get_engine_for_chinook_db()
    
    # Create a LangChain SQLDatabase wrapper around the engine
    db = SQLDatabase(engine)
    
    return db
