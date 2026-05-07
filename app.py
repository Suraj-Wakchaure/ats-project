from flask import request, render_template, redirect, url_for, jsonify, Flask, flash, session
from fuzzywuzzy import fuzz
from datetime import datetime
from database import get_database, init_database
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
ADMIN_USER = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

@app.route('/')
def main_page():
    conn = get_database()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return render_template('landing_page.html', jobs=jobs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USER and password == ADMIN_PASSWORD:
            session['user'] = username
            return redirect(url_for('jobs_page'))
        else:
            flash('Invalid credentials.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You logged out!')
    return redirect(url_for('main_page'))

#render the job page
@app.route('/jobs')
def jobs_page():
    if 'user' not in session:
        flash('Please login!')
        return redirect(url_for('login'))
    conn = get_database()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return render_template('jobs_page.html', jobs=jobs)

#render the candidate page
@app.route('/candidates')
def candidates_page():
    if 'user' not in session:
        flash('Please login!')
        return redirect(url_for('login'))
    
    conn = get_database()
    
    candidates = conn.execute('SELECT * FROM applications ORDER BY score DESC').fetchall()
    conn.close()
    return render_template('candidates_page.html', candidates=candidates)

#render the notifications page
@app.route('/notifications')
def notifications_page():
    if 'user' not in session:
        flash('Please Login!')
        return redirect(url_for('login'))
    conn = get_database()
    notifications = conn.execute(
        'SELECT * FROM notifications ORDER BY timestamp DESC'
    ).fetchall()
    conn.close()
    return render_template('notifications_page.html', notifications=notifications)

@app.route('/api/jobs', methods=["GET"])
def get_jobs():
    conn = get_database()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return jsonify([dict(row) for row in jobs])

@app.route('/api/jobs', methods=["POST"])
def create_jobs():
    if 'user' not in session:
        flash('Please login first')
        return redirect(url_for('login'))
    title = request.form.get('title', '').strip()
    required_skills = request.form.get('required_skills', '').strip()
    if not title or not required_skills:
        flash('title and skills are required')
        return redirect(url_for('jobs_page'))
    conn = get_database()
    conn.execute(
        'INSERT INTO jobs (title, skills_required) VALUES (?, ?)',
        (title, required_skills)
    )
    conn.commit()
    conn.close()
    flash('Job created!')
    return redirect(url_for('jobs_page'))


#function to calculate score
def calculate_score(required_skills, candidate_skills):
    required = [s.strip().lower() for s in required_skills.split(',')]
    candidate_skills = [s.strip().lower() for s in candidate_skills.split(',')]
    
    match_score = 0
    for skill in required:
        for candidate_skill in candidate_skills:
            if fuzz.ratio(skill, candidate_skill) > 80:
                match_score += 1
                break
    return round(match_score/len(required) * 100, 2)

@app.route('/apply/<int:job_id>')
def apply_page(job_id):
    conn =  get_database()
    job = conn.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    conn.close()
    if not job:
        flash('Job not found')
        return redirect(url_for('main_page'))
    return render_template('apply_page.html', job=job)

@app.route('/apply', methods=['POST'])
def apply():
    candidate_name = request.form.get('candidate_name', '').strip()
    email = request.form.get('email', '').strip()
    skills = request.form.get('skills', '').strip()
    job_id = request.form.get('job_id', type=int)


    if not candidate_name or not email or not skills or not job_id:
        flash('All fields required')
        return redirect(url_for('jobs_page'))
    
    conn = get_database()
    
    job = conn.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    if not job:
        flash('Job not found')
        conn.close()
        return redirect(url_for('jobs_page'))
    
    applied = conn.execute('SELECT id FROM applications WHERE email = ? and job_id = ?', (email, job_id)).fetchone()
    
    if applied:
        flash('You have already applied')
        conn.close()
        return redirect(url_for('jobs_page'))
    
    score = calculate_score(job['skills_required'], skills)
    applied_at = datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn.execute('INSERT INTO applications (candidate_name, email, skills, score, applied_at, job_id) VALUES (?, ?, ?, ?, ?, ?)', (candidate_name, email, skills, score, applied_at, job_id))
    
    conn.execute('INSERT INTO notifications (message, timestamp, job_id) VALUES(?,?,?)',(f"Application from {candidate_name} for {job['title']}", timestamp, job_id))
    
    conn.commit()
    conn.close()

    flash(f'Applied successfully! Your score is {score}%')
    return redirect(url_for('main_page'))


@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    conn = get_database()
    notifications = conn.execute('SELECT * FROM notifications ORDER BY timestamp DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in notifications])


@app.route('/notifications/<int:notification_id>/read', methods=['POST'])
def mark_as_read_page(notification_id):
    if 'user' not in session:
        flash('Please login first')
        return redirect(url_for('login'))
    conn = get_database()
    conn.execute('UPDATE notifications SET is_read = 1 WHERE id = ?', (notification_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('notifications_page'))


@app.route('/notifications/<int:notification_id>/unread', methods=['POST'])
def mark_as_unread_page(notification_id):
    if 'user' not in session:
        flash('Please login first')
        return redirect(url_for('login'))
    conn = get_database()
    conn.execute('UPDATE notifications SET is_read = 0 WHERE id = ?', (notification_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('notifications_page'))

init_database()
if __name__ == '__main__':
    app.run(debug = True)    