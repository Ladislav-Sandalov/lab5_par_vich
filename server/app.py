from flask import Flask
from server.routes.employees import employees_bp
from server.routes.halls import halls_bp
from server.routes.warehouse import warehouse_bp
from server.routes.orders import orders_bp


app = Flask(__name__)

# Регистрация маршрутов
app.register_blueprint(employees_bp, url_prefix='/employees')
app.register_blueprint(halls_bp, url_prefix='/halls')
app.register_blueprint(warehouse_bp, url_prefix='/warehouse')
app.register_blueprint(orders_bp, url_prefix='/orders')
# Главная страница
@app.route('/')
def index():
    return "Welcome to the Restaurant Management System API!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)