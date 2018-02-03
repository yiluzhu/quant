import os

from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    #print('--------cwd', os.getcwd(), 'list dir', os.listdir('.'))
    print('--------env', os.environ)
    print('--------tcl/', [root+str(files) for root, dirs, files in os.walk('/home/vcap/deps/0/python/') if 'init.tcl' in files])
    #print('--------tcl3/', os.listdir('/home/vcap/deps/0/python/tcl/tcl8.6/'))
    return 'Test finished'


#
if __name__ == '__main__':
    app.run(debug=True)
