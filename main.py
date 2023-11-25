from flask import Flask, request, jsonify, render_template, request, redirect, url_for
import redis
import json

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_job():
    # Generate a new job ID
    job_id = redis_client.incr('job_id')
    new_job = {
        'id': job_id,
        'title': request.form['title'],
        'company': request.form['company'],
        'status': request.form['status']
    }

    redis_client.hset(f'job:{job_id}', mapping=new_job)
    return jsonify(new_job), 201


@app.route('/jobs')
def get_jobs():
    # Fetch all job IDs
    job_ids = redis_client.lrange('jobs', 0, -1)

    jobs = []
    for job_id in job_ids:
        job_data = redis_client.hgetall(f'job:{job_id.decode("utf-8")}')
        jobs.append({key.decode("utf-8"): value.decode("utf-8") for key, value in job_data.items()})

    return jsonify(jobs)


if __name__ == '__main__':
    app.run(debug=True)
