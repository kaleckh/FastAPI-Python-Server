# Twitter Dupe Backend

## Overview
The backend for the Twitter Dupe app is built using **FastAPI**, a scalable and high-performance API for the social media application. It handles user authentication, tweet management, comments, likes, and other backend logic. The backend is integrated with a **PostgreSQL database** and designed to support a modern and efficient frontend.

---

## Features
- **Tweet Management:** Create, retrieve, update, and delete tweets.
- **Comment System:** Support for nested comments.
- **Like Functionality:** Manage likes and unlikes for tweets.
- **Database Integration:** PostgreSQL for persistent storage with SQLAlchemy as the ORM.

---

## Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Server:** Uvicorn (ASGI server for FastAPI)
- **Deployment:** Docker, Vercel, or traditional hosting platforms

---

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL
- Virtual Environment (optional but recommended)

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/kaleckh/FastAPI-Python-Server.git
   cd twitter-dupe-backend
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database:**
   - Create a PostgreSQL database.
   - Update the database URL in `config.py` or as an environment variable:
     ```bash
     export DATABASE_URL="postgresql://username:password@localhost:5432/twitter_dupe"
     ```

5. **Run Database Migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start the Server:**
   ```bash
   uvicorn app:main --host 0.0.0.0 --port 8000
   ```
---


## Environment Variables
Ensure the following environment variables are set:
- `DATABASE_URL`: PostgreSQL local connection string.
- `DIRECT_URL`: PostgreSQL prod connection string.
- `SUPABASE_KEY`: Supabase API key.

---

## Future Improvements
- Add support for image and video uploads.
- Implement advanced analytics and activity tracking.
- Optimize database queries for high-traffic scenarios.



## Contact
For any questions or inquiries, reach out to:
- **Email:** your.kaleckh@gmail.com
- **GitHub:** [https://github.com/kaleck]
- **LinkedIn:** [https://linkedin.com/in/kaleck-hamm]

