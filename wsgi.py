# -*- coding: utf-8 -*-
"""
WSGI entrypoint for Cloud Production Deployment
"""
from app import app

if __name__ == "__main__":
    app.run()
