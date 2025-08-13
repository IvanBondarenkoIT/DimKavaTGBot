#!/usr/bin/env python3
"""
Главный файл приложения для Railway
"""

import os
from bot.__main__ import app

if __name__ == "__main__":
    # Railway автоматически устанавливает переменную PORT
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
