# Business Manager: Business Management System with Django

## Table of Contents
[Description](#description)
[Features](#features)
[Technologies](#tecnologies)
[Installation](#instalation)
[Project Structure](#project)
[License](#license)
[Contact](#contact)

## Description
Business Manager is a comprehensive Django web application designed to streamline business administration tasks. It provides an integrated solution for managing appointments, clients, employees, sales, 
services, and inventory.

## Features
- 📅 Advanced appointment scheduling
- 👥 Client and employee management
- 💼 Sales tracking and reporting
- 🛒 Service catalog management
- 📦 Real-time inventory control
- 🔐 Secure user authenticationç
  
## Technologies
### Backend
- Django 5.1
- Python 3.12
- SQLite (development)
- Django Debug Toolbar
  
### Frontend
- Bootstrap 5.3
- jQuery 3.7.0
- Select2
- FullCalendar
- Flatpickr

## Installation
### Prerequisites
- Python ~=3.12
- pip
- virtualenv

### Setup
- Clone the repository
```
git clone https://github.com/yourusername/business-manager.git
cd business-manager
```
- Create virtual environment
```
python -m venv venv
Linux/Mac source venv/bin/activate
Windows venv\Scripts\activate
```
- Install dependencies
```
pip install -r requirements.txt
```
- Configure database
```
python manage.py migrate
```
- Create superuser
```
python manage.py createsuperuser
```
- Run development server
```
python manage.py runserver
```

## Project Structure
```
business-manager/
│
├── appointment/     # Appointment management
├── client/          # Client management
├── employee/        # Employee management
├── sales/           # Sales tracking
├── service/         # Service catalog
└── stock/           # Inventory management
```

## License
Copyright © 2025 <copyright holders>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject 
to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Contact
- Mónica González
- mgbarreto@outlook.es
- Project Link: https://github.com/Monikgbar/business-manager
