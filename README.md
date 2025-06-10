#  FastAPI App

This is a RESTful API built with **FastAPI**, featuring user registration, login, JWT authentication, and CRUD operations for posts. It's structured to be clean, scalable, and ready for deployment.

##  Features

- ✅ User Registration and Login (with hashed passwords)
- 🔐 JWT Authentication
- 🧾 Create, Read, Update, Delete Posts
- 🙋‍♂️ Get Current Authenticated User
- 🌍 CORS Support for API Access Across Domains

##  Tech Stack

- **Python 3.12**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **Uvicorn**
- **SQLite (or PostgreSQL ready)**
- **OAuth2 Password Flow**
- **JWT (via PyJWT)**

## ⚙️ Getting Started Locally

### 1. Clone the Repository

 bash
git clone https://github.com/kadafa11/fastapi-app.git
cd fastapi-app
2. Create and Activate a Virtual Environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Run the Server
uvicorn app:app --reload
The API will be available at http://127.0.0.1:8000

🔐 Authentication
Method	Endpoint	Description
POST	/api/v1/users	Register a new user
POST	/api/v1/login	Login and get token
GET	/api/v1/users/current-user	Get current user info

📝 Posts
Method	Endpoint	Description
POST	/api/v1/posts	Create new post
GET	/api/v1/posts/user	Get user's posts
GET	/api/v1/posts/all	Get all posts
GET	/api/v1/posts/{post_id}/	Get single post
PUT	/api/v1/posts/{post_id}/	Update a post
DELETE	/api/v1/posts/{post_id}/	Delete a post

🧪 Testing the API
Open your browser at:http://127.0.0.1:8000/docs
FastAPI comes with automatic Swagger UI documentation.

🛰 Deployment
You can deploy this project to platforms like:
Render
Railway
Fly.io
Heroku (requires payment method)
VPS / Ubuntu server

🙋‍♀️ Author
Created by @kadafa11

