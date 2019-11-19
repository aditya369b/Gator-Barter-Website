"""
File that the server uses to deploy the app, 
DO NOT TOUCH
"""
from app import app

if __name__ == "__main__":
    app.run("0.0.0.0")
