Introduction to Business Manager
================================

**Business Manager** is a comprehensive Django-based web application designed to streamline and automate various aspects
of business administration. This project provides an integrated solution for managing clients, appointments, employees,
sales, services, and inventory, catering to the needs of modern businesses.


Key Features
------------
- User-friendly interface for efficient task management
- Robust appointment scheduling system
- Comprehensive client and employee management
- Integrated sales tracking and reporting
- Service catalog management
- Real-time inventory control


Installation
------------
To set up Business Manager, follow these steps:

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/Monikgbar/business_manager
      cd business-manager

2. Create and activate a virtual environment:

   .. code-block:: bash

      python -m venv venv
      Linux/Mac source venv/bin/activate
      Windows venv\Scripts\activate

3. Install the required dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

4. Run migrations:

   .. code-block:: bash

      python manage.py migrate

5. Create a superuser:

   .. code-block:: bash

      python manage.py createsuperuser

6. Start the development server:

   .. code-block:: bash

      python manage.py runserver

Visit `http://localhost:8000` in your browser to access the application.


Dependencies
------------
The following dependencies are required to run the Business Manager project:

Python Libraries
----------------
These libraries are installed automatically via ``pip install -r requirements.txt``:

- **Django** >= 5.1.2: The core framework for the project.
- **django-debug-toolbar**: For debugging and performance analysis during development.
- **openpyxl**: For reading and writing Excel files(.xlsx)
- **xlwt**: For writing Excel files in old format(.xls)
- **xlrd**: For reading files in old format(.xls)

JavaScript and CSS Libraries (via CDN)
--------------------------------------
The following libraries are loaded via CDN in the HTML templates:

- **Bootstrap 5.3.0**
    - CSS: ``https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css``
    - JS: ``https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js``
- **Bootstrap Icons 1.8.1**
    - CSS: ``https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.8.1/font/bootstrap-icons.min.css``
- **Select2 4.1.0-rc.0**
    - CSS: ``https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css``
    - JS: ``https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js``
- **Flatpickr**
    - CSS: ``https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css``
    - JS: ``https://cdn.jsdelivr.net/npm/flatpickr``
- **FullCalendar 6.1.15**
    - CSS: ``https://cdn.jsdelivr.net/npm/fullcalendar@6.1.15/index.global.min.css``
    - JS: ``https://cdn.jsdelivr.net/npm/fullcalendar@6.1.15/index.global.min.js``
- **jQuery 3.7.0**
    - JS: ``https://code.jquery.com/jquery-3.7.0.min.js``

System Requirements
-------------------
Ensure the following are installed on your system:

* Python >= 3.12
* pip (Python package manager)
* Git (for cloning the repository)


Project structure
------------------
Business Manager is composed of several Django applications, each responsible for a specific aspect of business
management:

- **appointment**: Manages scheduling and tracking of appointments
- **client**: Handles client information and interactions
- **employee**: Oversees employee data and performance metrics
- **sales**: Tracks sales transactions and generates reports
- **service**: Manages the catalog of services offered
- **stock**: Controls inventory levels and product management

Each application is designed to work seamlessly with others, providing a cohesive business management solution.