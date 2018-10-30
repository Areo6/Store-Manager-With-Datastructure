from app import app
from app.api.db import Database


if __name__ == "__main__":
    db = Database()
    db.create_tables()
    app.run(debug=True)