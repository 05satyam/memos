from flask import Flask, request, jsonify, render_template, request, redirect, url_for
import redis
import json
import os
from urllib.parse import urlparse

app = Flask(__name__)
# url = urlparse(os.environ.get("REDIS_URL"))
# redis_client = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True, ssl_cert_reqs=None)

url = urlparse(os.environ.get('REDISCLOUD_URL'))
redis_client = redis.Redis(host=url.hostname, port=url.port, password=url.password)



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
    print("new_job ", new_job)
    redis_client.hset(f'job:{job_id}', mapping=new_job)
    return render_template('index.html')


@app.route('/')
def get_jobs():
    # Fetch all job IDs
    job_ids = redis_client.lrange('jobs', 0, -1)
    print()
    jobs = []
    for job_id in job_ids:
        job_data = redis_client.hgetall(f'job:{job_id.decode("utf-8")}')
        jobs.append({key.decode("utf-8"): value.decode("utf-8") for key, value in job_data.items()})

    print(jobs)
    return render_template('index.html', jobs=jobs)


if __name__ == '__main__':
    app.run(debug=True)
