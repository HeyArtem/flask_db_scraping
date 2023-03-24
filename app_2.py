from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request  
from datetime import datetime


"""
Тренируюсь с SQLAlchemy
Создам в БД две таблицы
Users и Profiles, м/у собой связаны по id
"""


# Создаю экземпляр приложения
app = Flask(__name__)

# Создаю конфигурацию, константу "SQLALCHEMY_DATABASE_URI". Эта константа, будет определять вид используемой БД и местоположение
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

# Создаю экземпляр класса SQLAlchemy, через который и осуществляется работа с БД.
db = SQLAlchemy(app)

# Концепция SQLAlchemy, заключается в отображении таблиц с помощью классов
# Создам две таблицы

# Класс Users наследется от класса Model, который превращает модель таблицы для  SQLAlchemy
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=False) # nullable=False - не позволяет полю быть пустым
    date = db.Column(db.DateTime, default=datetime.utcnow)

    pr = db.relationship('Profiles', backref='users', uselist=False)
 
    # метод будет отображать класс в консоли в фомате "users id"
    def __repr__(self):
        return f"<users {self.id}>"
    

class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))
 
    # Внешний ключ, связь Profiles & Users
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
 
    def __repr__(self):
        return f"<profiles {self.id}>"


@app.route("/")
def index():
    info = []
    try:
        info = Users.query.all()
    except:
        print("Ошибка чтения из БД")

    return render_template("index.html", title="Главная", list=info)
    

# Обработчик регистрации пользователей
@app.route("/register", methods=("POST", "GET"))
def register():

    # Добавление записи в БД
    if request.method == "POST":        
        try:
            # Из формы взял пароль пользователя введеный при регистрации
            hash = generate_password_hash(request.form['psw'])

            # Создал экз-р класса Users, передал именов пра-ры экз-ру этого класса
            u = Users(email=request.form['email'], psw=hash)

            # Обращаюсь к объекту session, вызываю метод add,которому передаю ссылку, на созданный экз класса users (запись пока в памяти устройства)
            db.session.add(u)

            # flush() - перемещает запись из ссесии в таблицу (запись пока в памяти устройства)
            db.session.flush()

            # Добавление записи в табл Profiles.Создаю экз класса, передаю именованные параметры
            p = Profiles(name=request.form['name'], old=request.form['old'],
                         city=request.form['city'], user_id = u.id)  # u.id-взял из   экз класса Users
            
            # Перемещаю запись в табл Profiles
            db.session.add(p)

            # метод commit() физически меняет БД и сохраняет изменения в таблицах 
            db.session.commit()

        # Если при добавлении данныз произошли ошибки, откатываю состояние БД
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")

        # return redirect(url_for('index'))
    
    return render_template("register.html", title="Регистрация")
    

    

if __name__ == "__main__":
    app.run(debug=True)
