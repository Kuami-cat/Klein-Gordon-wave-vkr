"""
Flask веб-приложение для решения обобщённого уравнения Клейна-Гордона с диссипацией
"""

import matplotlib
matplotlib.use('Agg')

from flask import Flask
from routes import register_routes

app = Flask(__name__)
register_routes(app)

if __name__ == '__main__':
    print("Откройте: http://127.0.0.1:5000")
    print("Для остановки нажмите Ctrl+C")

    app.run(debug=True, host='127.0.0.1', port=5000)