# GiftMatch: Smart Gift Suggestion System

GiftMatch is a responsive, desktop-first web application that helps users find thoughtful gift ideas based on recipient type, occasion, interests, budget, and preferred marketplace. The user-facing website is designed like a polished consumer product with a clean landing page, guided gift finder, dashboard, wishlist, occasion reminders, notifications, and recommendation system.

---

## ✨ Main Features

- Register, login, logout, user profile, and edit profile
- Google and Facebook social-login integration using django-allauth
- Desktop-first landing page, dashboard, gift finder wizard, and recommendation pages
- Poppins font, hover effects, modern cards, and responsive layout
- Recipient-based occasion filtering in the gift finder
- Visual interest cards with checkbox behavior
- Strict recommendation matching by recipient, occasion, interest, budget, and marketplace
- Match score and "Why this gift?" explanation for each recommendation
- Expanded demo catalog with 5,120 gift records and product-photo URLs
- Marketplace selection and links (Shopee, Lazada, TikTok Shop, Temu)
- Gift comparison feature (shown when at least two results are available)
- Wishlist with add, remove, planned, purchased status
- Occasion manager with countdown days and reminder settings
- Upcoming occasion cards open gift finder pre-filled
- Notification system with badge count, scrollable panel, mark-as-read actions
- About Us, Privacy Policy, Terms of Service, Contact pages
- GiftMatch Pro subscription page
- Progressive Web App (manifest, service worker, offline page, icons)
- Dockerfile and docker-compose.yml included

---

## 🧑‍💻 Developers

This project was developed by:

- Althea Lauren J. Villa
- Norelyn Madia
- Julius Arnesto
- Princess Heaven Rica

---

## 🌐 Live Demo

https://giftmatch.pythonanywhere.com

---

## 🛠 Technologies Used

- Python
- Django
- Django REST Framework
- django-allauth
- SQLite (default)
- HTML, CSS, JavaScript
- Custom responsive CSS
- Progressive Web App (PWA)
- Docker & Docker Compose

---

## 🚀 How to Run Without Docker

cd giftmatch_project
python -m venv .venv

Windows:
.venv\Scripts\activate

macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 8001

Open:
http://127.0.0.1:8001/

---

## 🐳 How to Run Using Docker

cd giftmatch_project
docker compose up --build

Open:
http://127.0.0.1:8000/

---

## 👤 Demo Accounts

Admin:
admin / admin12345

Demo:
sarah / demo12345

Admin Panel:
http://127.0.0.1:8001/admin/

---

## 🔌 API Notes for Instructor Checking

Internal API routes (hidden from UI):

/api/v1/gifts/
/api/v1/categories/
/api/v1/interests/
/api/v1/wishlist/
/api/v1/occasions/
/api/v1/notifications/
/api/v1/recommendations/
/api/v1/profile/

---

## 📱 PWA Support

/static/pwa/manifest.json
/static/pwa/service-worker.js
/static/images/icons/icon-192.png
/static/images/icons/icon-512.png
/offline/

---

## 📸 Screenshots

### Landing Page
<img width="1897" height="893" alt="image" src="https://github.com/user-attachments/assets/3dc29fa5-9846-4e42-a07b-a7841e182002" />

Figure 1. GiftMatch landing page.

### User Registration
<img width="1900" height="906" alt="Screenshot 2026-06-05 222449" src="https://github.com/user-attachments/assets/62a81050-7926-44bc-b079-1b5d9e3af05a" />

Figure 2. Registration page.

### User Login
<img width="1892" height="886" alt="Screenshot 2026-06-05 222519" src="https://github.com/user-attachments/assets/5f203854-da5f-4bcd-b011-8ea2c5fcf9ba" />

Figure 3. Login page.

### Gift Dashboard
<img width="1918" height="908" alt="Screenshot 2026-06-05 222729" src="https://github.com/user-attachments/assets/1e891fbe-ec40-4386-a50c-37f39b7dabb7" />

Figure 4. Dashboard page.

### Gift Finder
<img width="1903" height="896" alt="Screenshot 2026-06-05 223037" src="https://github.com/user-attachments/assets/d9ec8247-5ca3-4da8-80f3-4786b93c451d" />

Figure 5. Find match gift.

### Occasions
<img width="1885" height="897" alt="Screenshot 2026-06-05 223114" src="https://github.com/user-attachments/assets/693940f2-c92b-424b-b14b-7d26c8fae843" />

Figure 6. Choose what occasions.

### Details
<img width="1919" height="911" alt="Screenshot 2026-06-05 223254" src="https://github.com/user-attachments/assets/d868bc12-3608-472b-acf4-2d194dc1fb8c" />

Figure 7. Choose what's the interest, budget, and marketplace.

### Recommendations
<img width="1899" height="901" alt="Screenshot 2026-06-05 223426" src="https://github.com/user-attachments/assets/81783631-b73c-4626-a780-fccc8a51b7d0" />

Figure 8. Found relevant matches.


### Wishlist
<img width="1907" height="886" alt="Screenshot 2026-06-05 223536" src="https://github.com/user-attachments/assets/ed14f0a0-b685-4e4f-aef9-8c51a614cf28" />

Figure 9. Save gift ideas, remove them, or mark them as purchased.

### GiftMatch Pro
<img width="1875" height="885" alt="Screenshot 2026-06-05 223738" src="https://github.com/user-attachments/assets/b4425763-e41d-4f02-9d60-407eaef9553d" />

Figure 10. Upgrade gifting experience.

### Profile
<img width="1881" height="902" alt="Screenshot 2026-06-05 223956" src="https://github.com/user-attachments/assets/94dbb540-6ea3-4330-abe7-8f4dcaf68110" />


Figure 10. Profile page.


---

## ⚠️ Important Notes

- Run `python manage.py seed_demo` after setup to load full gift catalog with images
- If images don’t appear, reset DB and rerun migrations + seed_demo
- Social login requires valid OAuth credentials in .env

