from app import app

if __name__ == "__main__":
    app.run()

# We can test gunicorn's ability to serve our project 
# by running the command below: gunicorn --bind 0.0.0.0:5000 wsgi:app