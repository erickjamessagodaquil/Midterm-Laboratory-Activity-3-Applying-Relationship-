from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

# 1. Database URL (SQLite for simplicity, change as needed)
DATABASE_URL = "sqlite:///./mydatabase.db"  # Relative path

# 2. Declarative Base
Base = declarative_base()

# 3. Database Model
class MyModel(Base):
    __tablename__ = "mymodels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

# 4. Create Engine and Tables (CLI equivalent)
engine = create_engine(DATABASE_URL)

# CLI Equivalent (using Python code)

def create_database_and_tables():
  """Creates the database and tables."""
  Base.metadata.create_all(bind=engine)
  print("Database and tables created.")

def seed_database():
    """Seeds the database with sample data."""
    with Session(engine) as session:
        model1 = MyModel(name="Example 1", description="This is an example.")
        model2 = MyModel(name="Example 2", description="Another example.")
        session.add_all([model1, model2])
        session.commit()
    print("Database seeded.")

def query_database():
    """Queries and prints data from the database."""
    with Session(engine) as session:
        results = session.query(MyModel).all()
        for result in results:
            print(f"ID: {result.id}, Name: {result.name}, Description: {result.description}")

if __name__ == "__main__":
    create_database_and_tables()
    seed_database()
    query_database()