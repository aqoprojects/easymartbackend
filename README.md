# EasyMart Backend 

Easy mart is a full-featured e-commerce web application designed to connect buyers and vendors in a secure, user-friendly marketplace. The platform allows users to sign up, log in, and explore a wide range of products organized by categories and subcategories.

Users can easily add items to their cart, save shipping information, and manage billing or home addresses for faster checkout. The platform supports multiple payment options, including credit/debit cards, cryptocurrency, and online bank transfers, giving customers flexibility and convenience.

Beyond shopping, users can become vendors and own personal stores, enabling them to list products and manage orders. A built-in chat system allows direct communication between buyers and vendors, while an AI assistant is available for real-time support and inquiries.

To ensure trust and transparency, all customer payments are held securely by the company until both the buyer and vendor confirm successful product delivery. This guarantees fair transactions and enhances buyer protection.

The system also features a referral program, allowing users to earn rewards for inviting friends, and a review system for sharing feedback and building community trust.


## How to run

  ### Download EasyMart  
  - CLone: `https://github.com/aqoprojects/easymartbackend.git`

  ### INstallation & Setup
  1. Download python version 3.10 or above.
  2. Open EasyMart on IDE (vs code, pycharm).
  3.  Run this CMD `pip install -r requirements.txt`.

  ### Database Setup & Migration
  1. Download and install xampp (for faster and easy setup).
  2. Launch xampp, click the start button under Actions on the same row as Apache and MYSQL, text chnages to stop.
  3. Now, on the same row as MYSQL click the Admin button (it opens your web broswe and takes you to an admin page to create and manage databases).
  4. create a new database
  5. in EasyMart, goto easymart/settings.py scroll down and change db settings:
    - NAME: your created db name
    - USER: root (if you are running local on your pc)
    - PASSWORD: '' (empty strings)
    - HOST: '127.0.0.1' (default)
    - PORT: 3306 (default)
    - Configure EMAIL settings, Background task & Mesage broker, Redis cache
  6. in EasyMart terminal run this CMD `python manage.py makemigrations` && `python manage.py migrate`


  ## Start Server

  1. Run CMD `python manage.py runserver`
  2. goto your web browser
  2. in url bar, type `http://localhost:8000`


## Features
1. Authentication 
  - Customer Registrations, Customer Verification, Customer Login, Oauth, 2FA
2. Preference
  - Customer preference 
- New Feature to be added in next commit 

## Technologies & Requirements

| Technologies | Description |
|--------------|-------------|
| Python       | Programming Language |
| Django       | Robust Backend Framework |
| DRF          | Robust REST API Framwork |
| JWT          | Authentication |
| Celery & RabbitMQ | Background Task & Message Broker |
| Redis        | Efficient Data Caching |
| CloudFlare   | Storage |    

- As project continues more technologies will be added
