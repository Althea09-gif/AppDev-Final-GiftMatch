# GiftMatch: Smart Gift Suggestion System

GiftMatch is a responsive, desktop-first web application that helps users find thoughtful gift ideas based on recipient type, occasion, interests, budget, and preferred marketplace. The user-facing website is designed like a polished consumer product: clean landing page, guided gift finder, dashboard, wishlist, occasion reminders, notification bell, product details, and GiftMatch Pro page.

## Main Features

- Register, login, logout, user profile, and edit profile
- Google and Facebook social-login integration using django-allauth
- Desktop-first landing page, dashboard, gift finder wizard, and recommendation pages
- Poppins font, hover effects, modern cards, and responsive layout
- Recipient-based occasion filtering in the gift finder
- Visual interest cards with minimalist pink icons and checkbox behavior
- Strict recommendation matching by recipient, occasion, interest, budget, and marketplace
- Match score and "Why this gift?" explanation for each recommendation
- Expanded demo catalog with 5,120 gift records and product-photo URLs
- Marketplace selection and links for Shopee, Lazada, TikTok Shop, and Temu
- Gift comparison feature shown only when at least two results are available
- Wishlist with add, remove, planning-to-buy, and purchased status
- Occasion manager with guided placeholders, countdown days, and reminder settings
- Upcoming occasion cards can open the gift finder with details pre-filled
- Professional notification bell with count badge, scrollable panel, clear all, and mark-as-read actions
- Consumer-friendly About Us, Privacy Policy, Terms of Service, and Contact pages
- GiftMatch Pro subscription page
- Progressive Web App manifest, service worker, offline page, and icons
- Dockerfile and docker-compose.yml included

## Technologies Used

- Python
- Django
- Django REST Framework
- django-allauth
- SQLite by default
- HTML, CSS, JavaScript
- Custom responsive CSS
- Progressive Web App files
- Docker and Docker Compose

## How to Run Without Docker

```bash
cd giftmatch_project
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 8001
```

Open the app at:

```text
http://127.0.0.1:8001/
```

Use port `8001` if port `8000` is already showing an older project.

## How to Run Using Docker

```bash
cd giftmatch_project
docker compose up --build
```

Open the app at:

```text
http://127.0.0.1:8000/
```

## Demo Accounts

The `seed_demo` command creates these accounts:

```text
Admin username: admin
Admin password: admin12345

Demo username: sarah
Demo password: demo12345
```

Admin panel:

```text
http://127.0.0.1:8001/admin/
```

## Important Note About Product Images

Recommendation cards use product-photo URLs saved in the database through:

```bash
python manage.py seed_demo
```

If you previously ran an older copy of the project and still see text-only SVG placeholders, run:

```bash
python manage.py seed_demo
```

The command resets the demo gift catalog and reloads gifts with matched product photos. You can also delete `db.sqlite3`, run migrations again, then run `seed_demo` for a completely fresh database.

## Social Login Setup

The code includes django-allauth with Google and Facebook providers. For real Google/Facebook login, replace the placeholder OAuth credentials in `.env` or `.env.example`:

```text
SITE_DOMAIN=127.0.0.1:8000
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FACEBOOK_CLIENT_ID=your-facebook-client-id
FACEBOOK_CLIENT_SECRET=your-facebook-client-secret
```

Then run:

```bash
python manage.py seed_demo
```

The demo command creates/updates the SocialApp records using those environment values. Without real OAuth credentials, Google/Facebook will reject the placeholder client IDs.

## Main Web Pages

```text
/                         Landing Page
/accounts/login/          Login Page
/accounts/register/       Register Page
/dashboard/               Dashboard
/gifts/finder/            Gift Finder
/recommendations/         Gift Recommendations
/gifts/<id>/              Gift Details
/wishlist/                Wishlist
/occasions/               Occasion Manager
/notifications/           Notifications
/accounts/profile/        Profile
/pro/                     GiftMatch Pro
/about/                   About Us
/privacy/                 Privacy Policy
/terms/                   Terms of Service
/contact/                 Contact Us
/offline/                 PWA Offline Page
```

## API Notes for Instructor Checking

API routes still exist internally for project requirements, but they are intentionally hidden from the normal user interface because customers do not need to see developer-facing tools.

```text
/api/v1/gifts/
/api/v1/categories/
/api/v1/interests/
/api/v1/wishlist/
/api/v1/occasions/
/api/v1/notifications/
/api/v1/recommendations/
/api/v1/profile/
```

## PWA Support

Included PWA files:

```text
/static/pwa/manifest.json
/static/pwa/service-worker.js
/static/images/icons/icon-192.png
/static/images/icons/icon-512.png
/offline/
```

## Screenshots

Add your screenshots here after running the system:

- Landing Page
- Dashboard
- Gift Finder
- Recommendations
- Wishlist
- Occasion Manager
- GiftMatch Pro

## Required Lessons Shown in This Project

- Django Core: Models and ORM through UserProfile, Gift, Category, Interest, Occasion, WishlistItem, RecommendationHistory, and Notification models
- Django Core: Views and Authentication through protected pages and Django auth
- Progressive Web App through manifest, service worker, icons, and offline page
- API Integration in Django using external product data with fallback links
- RESTful API Development through Django REST Framework serializers, viewsets, and API routes
- Containerization using Dockerfile and docker-compose.yml
