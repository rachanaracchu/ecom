# CodeAlpha Task 1 - Simple E-commerce Store

## Ready-to-use features
- 8 products are automatically inserted into the database when migrations are run, with bundled product images displayed immediately.
- Product listing and product details
- Shopping cart
- User registration, login and logout
- Checkout and order processing
- SQLite database
- Django admin
- Responsive HTML/CSS/JavaScript frontend

## Run locally
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

After `migrate`, the 8 sample products automatically appear on the home page.

## Admin
Create an admin account:
```bash
python manage.py createsuperuser
```
Then open `/admin/`.

## Important: How others can view the project
A ZIP file is source code only. Uploading it to a submission portal lets evaluators inspect or run the code, but it does not automatically create a public website.

To give a live link, deploy the project to a Python hosting service such as Render. This project includes `Procfile` and `render.yaml` to help deployment. For production, configure environment variables such as `SECRET_KEY`, `DEBUG=False`, and `ALLOWED_HOSTS`.
