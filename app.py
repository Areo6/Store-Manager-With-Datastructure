from app import app
from database.db import Database


if __name__ == "__main__":
    db = Database()
    db.create_tables()
    db.create_admin()
    app.run(debug=True)