# 🏠 Real Estate Website (Django)

A full-stack **Real Estate Web Application** built using **Django** and deployed on **Render** with a **PostgreSQL** database.  
The platform allows users to browse property listings with images and provides an admin dashboard for managing data.

---

## 🚀 Live Demo

🔗 **Live URL:**  
https://real-estate-website.onrender.com  
> _(Replace this with your actual Render URL if different)_

---

## 🛠️ Tech Stack

- **Backend:** Django 5+
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** PostgreSQL (Render – Production)
- **Local Database:** SQLite (Development only)
- **Static Files:** WhiteNoise
- **Image Handling:** Pillow
- **Deployment:** Render (Gunicorn)
- **Version Control:** Git & GitHub

---

## ✨ Features

- User authentication (login & signup)
- Property listings with images
- Multiple images per property
- Admin panel for managing listings
- PostgreSQL database in production
- Secure production-ready settings
- Cloud deployment with auto-redeploy

---

## 📂 Project Structure

Real_Estate_Website/
│
├── manage.py
├── build.sh
├── render.yaml
├── requirements.txt
│
├── real_estate_project/
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── ...
│
├── users/
├── listings/
└── templates/


---

## ⚙️ Environment Variables (Production)

Configured in **Render Dashboard**:

| Variable | Description |
|--------|------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Set to `False` |
| `DATABASE_URL` | PostgreSQL connection string |

---

## 🗄️ Database Configuration

- **Production:** PostgreSQL (Render managed)
- **Local Development:** SQLite (fallback)
- Database migrations run automatically during deployment

---

## 📸 Image Uploads

- Uses Django `ImageField`
- Requires **Pillow** (included in `requirements.txt`)
- ⚠️ Uploaded media files are ephemeral on Render  
  👉 For production apps, use **Cloudinary** or **AWS S3**

---

## 🧑‍💻 Run Locally (Development)

1️⃣ Clone Repository
`
git clone https://github.com/Eswar0474/Real_Estate_Website.git
cd Real_Estate_Website`

2️⃣ Create Virtual Environment
`python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate`

3️⃣ Install Dependencies
`pip install -r requirements.txt`

4️⃣ Apply Migrations
`python manage.py migrate`

5️⃣ Create Admin User
`python manage.py createsuperuser`

6️⃣ Run Server
`python manage.py runserver`


Open in browser:
👉 http://127.0.0.1:8000/

🔐 Admin Panel

Access the Django admin panel at:

/admin


Login using the superuser credentials.

🚀 Deployment (Render)

Uses render.yaml Blueprint

Gunicorn as WSGI server

PostgreSQL auto-provisioned

Auto-deploy on GitHub push

Static files handled via WhiteNoise

📌 Important Notes

❌ Do NOT commit db.sqlite3

✅ PostgreSQL is used in production

🔁 Data persists across deployments

🧼 Build cache cleared on redeploy

👨‍💻 Author

Eswar
GitHub: https://github.com/Eswar0474
