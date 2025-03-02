# from flask_script import Manager
from controller import create_app

# app = create_app('dev')
app = create_app('pro')


if __name__ == '__main__':
    app.run(threaded=True, host="0.0.0.0", port=5000)

