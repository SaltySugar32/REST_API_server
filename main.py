from app import app, database
import config
import routes

if __name__ == '__main__':
    database.create_all()
    app.run()

