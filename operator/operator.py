import pymongo
from flask import Flask, request
app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello_world():
    return 'Hello World'

@app.route('/post/',methods=['POST'])
def show_post():
    # show the post with the given id, the id is an integer
    print(request.get_json())
    return 'Post %d' % 666
if __name__ == '__main__':
    app.run(debug = True)