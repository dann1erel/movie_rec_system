import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Genre, GenreLikes, MovieLikes


# создает контекст оболочки, который добавляет экземпляр базы данных и модели в сеанс оболочки
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Genre': Genre, 'GenreLikes': GenreLikes, 'MovieLikes': MovieLikes}
    
