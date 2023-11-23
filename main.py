from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

jobs = []  # This will store our jobs

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job = request.form.get('job')
        jobs.append(job)
        return redirect(url_for('index'))
    return render_template('index.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
