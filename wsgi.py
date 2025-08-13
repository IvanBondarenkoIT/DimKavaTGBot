#!/usr/bin/env python3
"""
WSGI файл для Railway
"""

import os
from bot.__main__ import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting WSGI server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
