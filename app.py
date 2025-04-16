from flask import Flask, render_template, request, redirect
import redis
import os

app = Flask(__name__)
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = 6379
r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    choice = request.form['choice']
    r.incr(choice)
    return redirect('/results')

@app.route('/results')
def results():
    cats = r.get('Cats') or 0
    dogs = r.get('Dogs') or 0
    return render_template('result.html', cats=cats, dogs=dogs)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
