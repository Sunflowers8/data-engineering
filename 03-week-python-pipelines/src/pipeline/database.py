from sqlalchemy import create_engine


class DatabaseClient:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url)

    def get_engine(self):
        return self.engine