# ATS Lite - Applicant Tracking System

A web-based Applicant Tracking System built with Flask and SQLite.
Recruiters can post jobs and track candidates ranked by skill match score.

---

## Tech Stack

- Python 3
- Flask
- SQLite
- Jinja2
- HTML/CSS

---

## Features

- Admin login/logout (session based)
- Post jobs with required skills
- Candidates apply publicly (no login required)
- Skill match score calculated automatically
- Candidates ranked by score (highest first)
- Notifications on every application
- Mark notifications as read/unread

---

## Project Structure

```
ATS-Project/
├── app.py
├── api.py    
├── database.py
├── .env
├── requirements.txt
├── static/
│   └── style.css
├── uploads/
└── templates/
    ├── base.html
    ├── landing_page.html
    ├── login.html
    ├── jobs_page.html
    ├── apply_page.html
    ├── candidates_page.html
    └── notifications_page.html
```

---

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/Suraj-Wakchaure/ats-project.git
cd ats-project

### 2. Install dependencies
pip install -r requirements.txt

### 3. Create `.env` file
SECRET_KEY=your_secret_key_here

ADMIN_USERNAME=admin

ADMIN_PASSWORD=admin123

API_KEY=your_api_key

### 4. Run the app
python app.py

### 5. Visit in browser
http://127.0.0.1:5000

---

## Admin Credentials
Username: admin, 
Password: admin123

---

## API Endpoints

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| GET | `/` | Landing page | - |
| GET | `/login` | Admin login page | - |
| GET | `/logout` | Admin logout | - |
| GET | `/jobs` | Admin jobs dashboard | - |
| GET | `/api/jobs` | Get all jobs (JSON) | - |
| POST | `/api/jobs` | Create a job | `title, required_skills` |
| GET | `/apply/<job_id>` | Candidate apply page | - |
| POST | `/apply` | Submit application | `candidate_name, email, skills, job_id` |
| GET | `/candidates` | Candidates ranked by score | - |
| POST | `/candidates` | Filter candidates by min score | `min_score` |
| GET | `/notifications` | View notifications | - |
| POST | `/notifications/<notification_id>/read` | Mark as read | - |
| POST | `/notifications/<notification_id>/unread` | Mark as unread | - |
| GET | `/api/notifications` | Get all notifications (JSON) | - |

---

## How Skill Matching Works

1. Admin posts a job with required skills e.g. `python, flask, sql`
2. Candidate applies with their skills e.g. `python, flask`
3. System calculates score:
matched skills / required skills x 100
python + flask matched = 2/3 = 66.67%
4. Fuzzy matching handles typos and variations
5. Candidates ranked highest score first

---

## Bonus Features Implemented

- Filtering candidates by minimum score (score > X)
- AI-generated candidate summaries using Groq (Llama3)
- Resume upload support

## Bonus Features Used
- Groq API (Llama3) for AI candidate summaries
- fuzzywuzzy for intelligent skill matching (handles typos and variations)

---

## Deployment

Live URL: `https://SurajWakchaure.pythonanywhere.com`

---
