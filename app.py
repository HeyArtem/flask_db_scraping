from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shampo.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Это прописываю в консоли
# from app import app, db

# app.app_context().push()
# db.create_all()
# ctr + D выход


class Shampo(db.Model):
    __tablename__ = "Shampo"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, index=True)
    description = db.Column(db.String(120))
    price = db.Column(db.String(20))
    created = db.Column(db.String(30))

    # def __init__(self, name, description, price):
    #     self.name = name
    #     self.description = description
    #     self.price = price
    
    def __repr__(self):
        return f"name: {self.name} \ndescription: {self.description}"

@app.route("/")
def index():
    info = Shampo.query.all()

    return render_template("shampo.html", list=info)


@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        # created = datetime.now()            
        created = request.form["created"]

        print("  created:", request.form["created"])

        now = datetime.now()

        if request.form["created"]:
            created = request.form["created"]
            
        else:
            created = now.strftime("%d-%m-%Y")
        
        # print("58:  ", created)

        info = Shampo(name=name, description=description, price=price, created=created)
        # info = Shampo(name=name, description=description, price=price)   

        print("  created after info:", request.form["created"])     

        try:
            db.session.add(info)
            db.session.commit()
            
            return redirect("/")
        except:
            return "Ошибка ввода данных"
    else:
        return render_template("create.html")




# # Ф-я добавления товара
# def add_shampo(name, description):
#     data = Shampo(name, description)
#     db.session.add(data)
#     db.session.commit()

# try:
#     add_shampo(name, description)
        
# except NameError:
#     print("Ошибка ввода данных.")

# except:
#     print("Ошибка другого вида")


if __name__ == "__main__":
    app.run(debug=True)
