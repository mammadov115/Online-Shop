# Django Online Shop Application

The Django Online Shop Application is a comprehensive and feature-rich e-commerce solution designed to provide a seamless online shopping experience for users. This application empowers businesses to showcase their products, manage customer orders, and streamline the purchase process.

## Features

This Django Online Shop application comes with the following features:


- **Product Catalog:** Customers can browse and search for available products in a categorized catalog.

- **Shopping Cart:** Utilizing Django sessions, customers can add items to their cart, facilitating collection and the payment process.

- **Custom Context Processors:** Enhance the application by adding dynamic content through custom context processors.

- **Customer Order Management:** Users can track orders, view their status, and review previous order histories.

- **Celery and RabbitMQ Configuration:** Set up Celery to work in the application with RabbitMQ as a message broker.

- **Asynchronous Notifications:** Send asynchronous notifications to customers through Celery.

- **Flower Usage:** Monitor Celery tasks using the Flower monitoring tool.

- **Integration with Stripe Payment System:** Integrate the Stripe payment gateway into the application and handle credit card payments.

- **Payment Notification Management:** Manage notifications for successful and unsuccessful Stripe payments.

- **Export Orders to CSV Files:** Export order data to CSV files.

- **Custom Views for Admin Site:** Create custom views for the admin site.

- **Dynamic PDF Invoice Generation:** Dynamically generate PDF invoices.

- **Creating a Coupon System:** Implement a coupon system for applying discounts.

- **Applying Coupons to the Cart:** Allow users to apply coupons to their shopping cart.

- **Applying Coupons to Orders:** Apply coupons to orders for discounts.

- **Creating Coupons for Stripe Checkout:** Generate coupons for use with Stripe Checkout.

- **Storing Frequently Bought Together Products:** Store information about products often purchased together.

- **Building a Product Recommendation Engine with Redis:** Implement a product recommendation engine using Redis.

- **Preparing for Internationalization:** Prepare the project for translation and internationalization.

- **Managing Translation Files:** Manage translation files and translation processes.

- **Translating Python Code:** Translate Python code to support different languages.

- **Translating Templates:** Translate Django templates for different languages.

- **Using Rosetta for Translation Management:** Utilize Rosetta for managing translations.

- **Translating URL Patterns and Using Language Prefixes:** Translate URL patterns and implement language prefixes.

- **Allowing Users to Switch Language:** Implement language switching functionality for users.

- **Translating Models Using django-parler:** Translate models using the django-parler library.

- **Using Translations with the ORM:** Work with translated content using the Django ORM.

- **Adapting Views for Translations:** Adapt views to support translated content.

- **Using Localized Form Fields from django-localflavor:** Utilize localized form fields from django-localflavor for specific regions.


## Getting Started

Follow these instructions to set up the project on your local machine.

### Prerequisites

- Python: Make sure Python is installed on your system.
- Virtual Environment: Set up a Python virtual environment to manage dependencies.
- Django: Install Django in the virtual environment.

### Installation

1. Clone this repository to your local machine:

```bash 
git clone https://github.com/mammadov115/Online-Shop.git
```

2.  Create and activate a virtual environment:

```
python -m venv env
source env/bin/activate  
# On Windows, use: 
env\Scripts\activate
```

3. Install Django and other required packages:
``pip install -r requirements.txt``

4.  Set up the database and perform initial migrations:
``python manage.py migrate``

5. Create a superuser to access the admin panel:
``python manage.py createsuperuser``

6. Run the development server:
``python manage.py runserver``

7. Open your browser and go to:
``http://localhost:8000/``



## Contributing

If you have any feedback, suggestions, or would like to contribute, please create a new issue or submit a pull request.

### Thanks
