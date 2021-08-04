import os

from app import create_app

app = create_app(os.getenv('ENV', 'DEV'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
