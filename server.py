# new relic ping

import newrelic.agent
import _pickle as pickle
import os
from flask import Flask, render_template, request, abort, jsonify, url_for
from threading import Thread
import icarus

newrelic.agent.initialize('newrelic.ini')

# load autocomplete data into memory
AP_DATA = pickle.load(open('data/airports_data_dict.p', 'rb'))
AP_SEARCH = pickle.load(open('data/airports_search_arr.p', 'rb'))

app = Flask(__name__)

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

@async
def get_async_data(f, t, days):
    icarus.main(f, t, days)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    url_for('static', filename='viz.js')
    
    f = request.args.get('f', '')
    t = request.args.get('t', '')
    days = int(request.args.get('days', 0))

    # if ('f' in request.args):
    #     f = request.args['f']
    #     print('f: ' + request.args['f'])
    # if ('t' in request.args):
    #     t = request.args['t']
    #     print('t: ' + request.args['t'])
    # if ('days' in request.args):
    #     days = int(request.args['days'])
    #     print('days: ' + str(request.args['days']))

    name = '_'.join([f,t,str(days)])

    data = icarus.find(name)
    if data:
        return jsonify(**data)
    else:
        get_async_data(f, t, days)
        return name
    # return jsonify(**{'name': data['name'], 'data': data['data']})
    # get_async_data(f, t, days)

@app.route('/data/<name>.json')
def show_data(name):
    data = icarus.find(name)
    if data:
        return jsonify(**data)
    else:
        abort(404)

@app.route('/ac')
def autocomplete():
    q = request.args.get('q', '').lower()
    if not q:
        return ''

    suggestions = filter(lambda k: q in k, AP_SEARCH)
    suggestions = suggestions[:100]
    print('=========SUGGESTIONS==========')
    print(suggestions)
    results = []
    for k in suggestions:
        if AP_DATA[k] not in results:
            results.append(AP_DATA[k])

    results.sort(key=lambda k: k.lower().find(q))
    # results = results[:10]
    return jsonify(**{'query': 'Unit' , 'suggestions': results})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug = True, port=port, host='0.0.0.0')