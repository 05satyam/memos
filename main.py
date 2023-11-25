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
    for key in new_job:
        if not isinstance(new_job[key], str):
            new_job[key] = json.dumps(new_job[key])

    print("new_job ", new_job)
    redis_client.hset(f'job:{job_id}', mapping=new_job)
    return redirect(url_for('get_jobs'))


@app.route('/')
def get_jobs():
    # Fetch all job IDs
    job_ids = redis_client.keys('*')

    print("job_ids ", job_ids)
    decoded_job_ids = [job_id.decode('utf-8') if isinstance(job_id, bytes) and len(job_id.split(b':')) > 1 else job_id
                       for job_id in job_ids]

    print("decoded_job_ids ", decoded_job_ids)
    jobs = []
    for job_id in decoded_job_ids:
        print(f'{job_id}')
        job_data = redis_client.hgetall(f'{job_id}')
        print("job data ", job_data)
        retrieved_job = {key.decode('utf-8'): value.decode('utf-8') for key, value in job_data.items()}
        print("jretrieved_job ", retrieved_job)
        jobs.append(retrieved_job)

    print(jobs)
    return render_template('index.html', jobs=jobs)


if __name__ == '__main__':
    app.run(debug=True)
