#!/usr/bin/env python3
"""
Простой тестовый файл для Railway
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Тестовое приложение работает! 🚀"

@app.route('/test')
def test():
    return "Тестовая страница работает!"

if __name__ == "__main__":
    import os
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
