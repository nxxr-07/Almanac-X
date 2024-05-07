from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login import LoginManager
import requests
from bs4 import BeautifulSoup

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcdef'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('Website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created database!')


def scrape_updates():
    # Replace 'url' with the URL of your university website
    url = 'https://ptu.ac.in/noticeboard-main/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract relevant information from the table rows
        updates = []
        table = soup.find('table', class_='table')  # Replace 'updates-table' with the actual class name of the table
        if table:
            rows = table.find_all('tr')
            for row in rows[:5]:
                columns = row.find_all('td')
                if len(columns) >= 2:  # Assuming the title and description are in the first two columns
                    title = columns[0].text.strip()
                    date = columns[1].text.strip()
                    updates.append({'title': title, 'date': date})
        return updates
    else:
        return None



