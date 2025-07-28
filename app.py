from flask import Flask, render_template, request, redirect, url_for
import os
import csv
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'resumes'
CSV_FILE = 'submissions.csv'

# Create folders/files if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Email', 'Skills', 'Filename'])

# Homepage
@app.route('/')
def home():
    return render_template('home.html')

# Upload form
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        skills = request.form['skills']
        resume = request.files['resume']

        if resume.filename != '':
            filename = secure_filename(resume.filename)
            resume.save(os.path.join(UPLOAD_FOLDER, filename))

            # Save to CSV
            with open(CSV_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([name, email, skills, filename])

            return redirect(url_for('home'))

    return render_template('upload.html')

# Admin panel with skill search
@app.route('/admin')
def admin():
    data = []
    search_skill = request.args.get('skill', '').lower()

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not search_skill or search_skill in row['Skills'].lower():
                    data.append(row)

    return render_template('admin.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
