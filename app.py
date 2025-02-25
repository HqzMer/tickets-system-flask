from flask import Flask, render_template,Blueprint
from models import db
from routes_tickets import ticketsRouting

app = Flask(__name__)
app.register_blueprint(ticketsRouting)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'clave_secreta'  # Para formularios y sesiones

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)