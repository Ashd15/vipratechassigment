# VipraTech Django + Stripe Assignment

This is a complete Django project for the VipraTech assignment.

## What it does
- Shows 3 fixed products on a single page.
- User can input quantity and click Buy.
- Redirects to Stripe Checkout (test mode).
- After successful payment the paid order appears on the main page (My Orders).

## Setup (quick)
1. Copy `.env.example` to `.env` and fill STRIPE keys and SECRET_KEY.
2. Create and activate a virtualenv.
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py loaddata shop/fixtures/products.json`
6. `python manage.py runserver`

Visit http://127.0.0.1:8000/

Test card: 4242 4242 4242 4242 (any future expiry and CVC)

## Notes
- Uses Stripe Checkout to simplify handling and avoid double charges.
- Order model stores `checkout_session_id` uniquely to prevent duplicates.
- Optional: use `stripe listen` to enable webhook verification and set endpoint secret.

