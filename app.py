#!/usr/bin/env python3
"""
Главный файл приложения для Railway
"""

import os
from bot.__main__ import app

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
