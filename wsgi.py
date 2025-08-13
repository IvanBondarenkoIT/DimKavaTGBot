#!/usr/bin/env python3
"""
WSGI файл для Railway - обновленный интерфейс
"""

import os
from railway_interface_update import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting updated WSGI server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
