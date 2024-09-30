import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Like

# создает контекст оболочки, который добавляет экземпляр базы данных и модели в сеанс оболочки
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Like': Like}
    
