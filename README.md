# Restaurant kitchen service
Management system for improving the communication & rules between cooks on the kitchen.

## Check it out
[Restaurant kitchen service deployed to Render](https://restaurant-kitchen-service-p91s.onrender.com/)

To view the service on Render, use the following credentials:
```angular2html
username: test_user
password: SuperSecurePassword
```

## Introduction
Restaurant kitchen service is an innovative service designed to enhance communication between chefs and cooks. 
This platform offers a convenient way to distribute dishes among staff members, streamlining the entire cooking process. 
With this service, you can efficiently manage your kitchen and optimize work hours.

##### Two types of users:

* Chef: responsible for assigning dishes to cooks, add/update dish.
* Cook: can view dishes assigned to him, view cooks who can prepare a certain dish

##### Personalized pages:

Each Cook has their own page with a list of assigned dishes. Here, they can easily track tasks.
On the dish's page, cooks can see which Chefs can assign it for cooking, ensuring an optimal distribution of tasks.

##### Dish categories:

All dishes are organized into logical categories, simplifying search and organization.
Chefs can easily filter and find specific dishes to assign, while Cooks can quickly locate their assigned tasks.
FoodShare is where culinary masterpieces are created, and teamwork becomes easy and efficient. Join our community and help us turn cooking into a delightful experience!

## Getting Started

1. Clone the repository:
```angular2html
git clone https://github.com/imelnyk007/my-restaurant-kitchen-service.git
```
2. Create virtual environment:
```angular2html
python -m venv venv
source env/bin/activate 
```
3. Install requirements:
```angular2html
pip install -r requirements.txt
```
4. Make migration:
```angular2html
python manage.py migrate
```
5. Create a superuser:
```angular2html
python manage.py createsuperuser
```
6. Start server:
```angular2html
python manage.py runserver
```
