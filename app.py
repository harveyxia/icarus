import os
from flask import Flask, render_template, request
import icarus

app = Flask(__name__)

@app.route('/')
def index():
    # f = request.args['f'] or 'BOS'
    # t = request.args['t'] or 'LAX'
    # days = request.args['days'] or 3
    f = 'BOS'
    t = 'LAX'
    days = 3
    if ('f' in request.args):
        f = request.args['f']
        print('f: ' + request.args['f'])
    if ('t' in request.args):
        t = request.args['t']
        print('t: ' + request.args['t'])
    if ('days' in request.args):
        days = int(request.args['days'])
        print('days: ' + str(request.args['days']))

    prices = icarus.main(f, t, days)
    return render_template('index.html', prices = prices)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug = True, port=port)