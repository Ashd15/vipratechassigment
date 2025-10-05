VipraTech Django + Stripe Assignment

This is a Django project for the VipraTech assignment demonstrating product listing, Stripe payment integration, and order tracking.

Features

Display multiple products fetched from the backend database.

Users can input quantity for any product and click Buy.

Redirects to Stripe Checkout for payment (test mode).

After successful payment, the order appears on the main page (My Orders list).

Orders are tracked and displayed for the user.

Demo Flow

User visits the main page showing available products.

User selects quantity and clicks Buy.

Redirects to Stripe Checkout.

Upon successful payment, the order is recorded.

Users can view all their paid orders in My Orders.

Setup

Clone the repository:

git clone <repo_url>
cd <project_folder>


Copy the example environment file and fill in your keys:

cp .env.example .env


Add your STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY, and SECRET_KEY.

Note: If you are in India, Stripe may require an invite to create a test account and generate API keys.
Alternative: You can use a mock Stripe checkout for testing locally.

Create a virtual environment and activate it:

python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate


Install dependencies:

pip install -r requirements.txt


Run migrations:

python manage.py migrate


Load sample products:

python manage.py loaddata shop/fixtures/products.json


Run the development server:

python manage.py runserver


Open in browser:

http://127.0.0.1:8000/

Adding More Products

You can add as many products as you want via Django admin:

Create a superuser:

python manage.py createsuperuser


Login at http://127.0.0.1:8000/admin/

Add products with name, description, price, and image.

Stripe Integration Notes

Stripe Checkout is integrated for payments.

Test payments can be made using Stripe test cards.

For Indian users, Stripe may require an invite to access the test account.
If unable to register, you can:

Use Stripe mock server locally for testing.

Skip actual Stripe checkout and simulate a successful payment in the backend.

Tech Stack

Django (Backend)

SQLite (Database, default)

Stripe API (Payments)

HTML/CSS + Bootstrap (Frontend)