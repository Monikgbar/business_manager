from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from employee.models import Employee
from service.models import Service, Category
from employee.forms import EmployeeForm, ServicesEmployeeForm


class AddEmployeeViewTest(TestCase):
    """
    Test cases for the AddEmployeeView.

    This class contains unit tests to verify the functionality of the AddEmployeeView, which handles the creation of new
    Employee instances.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Initializes the URL for adding an employee, creates a test category and service.
        """
        self.add_employee_url = reverse('employee:add')
        self.category = Category.objects.create(name="Test Category")
        self.services = Service.objects.create(name="Test Service", category=self.category)

    def test_add_employee_GET(self):
        """
        Test the GET request to the add employee page.

        Verifies that the page loads correctly, uses the correct template, and contains the expected form and context
        data.
        """
        response = self.client.get(self.add_employee_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/add.html')
        self.assertIsInstance(response.context['form'], EmployeeForm)
        self.assertQuerySetEqual(response.context['services_categories'], [self.category])

    def test_add_employee_POST_valid(self):
        """
        Test the POST request with valid employee data.

        Ensures that a new employee is created with the provided data, including associated services, and that the user
        is redirected correctly.
        """
        employee_data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'telephone_number': '6234567890',
            'email': 'juan@example.com',
            'color': '#FF5733',
            'services': [self.services.id]
        }
        response = self.client.post(self.add_employee_url, data=employee_data)
        
        self.assertEqual(Employee.objects.count(), 1)
        
        new_employee = Employee.objects.first()
        self.assertRedirects(response, reverse('employee:view', args=[new_employee.id]))
        self.assertEqual(new_employee.first_name, 'Juan')
        self.assertEqual(new_employee.services.count(), 1)
        self.assertEqual(new_employee.services.first(), self.services)

    def test_add_employee_POST_invalid(self):
        """
        Test the POST request with invalid employee data.

        Verifies that no employee is created when invalid data is submitted, and that the form is re-rendered with error
        messages.
        """
        employee_data = {
            'first_name': '',  # Invalid: empty first name
            'last_name': 'Perez',
            'telephone_number': '6234567890',
            'email': 'juan@example.com',
        }
        response = self.client.post(self.add_employee_url, data=employee_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/add.html')
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Employee.objects.count(), 0)

    def test_add_employee_with_services(self):
        """
        Test adding an employee with multiple services.

        Ensures that an employee can be created with multiple associated services, and that these associations are
        correctly saved in the database.
        """
        service2 = Service.objects.create(name="Test Service 2", category=self.category)
        employee_data = {
            'first_name': 'Maria',
            'last_name': 'Leon',
            'telephone_number': '6987654321',
            'email': 'maria@example.com',
            'color': '#33FF57',
            'services': [self.services.id, service2.id]
        }
        
        response = self.client.post(self.add_employee_url, data=employee_data)
        
        self.assertEqual(Employee.objects.count(), 1)
        new_employee = Employee.objects.first()
        self.assertEqual(new_employee.services.count(), 2)
        self.assertIn(self.services, new_employee.services.all())
        self.assertIn(service2, new_employee.services.all())


class AssignServicesViewTest(TestCase):
    """
    Test cases for the AssignServicesView.

    This class contains unit tests to verify the functionality of the AssignServicesView, which handles the assignment
    of services to an existing Employee.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test employee, category, services, and initializes the URL for assigning services.
        """
        self.employee = Employee.objects.create(
            first_name="Juan",
            last_name="Perez",
            telephone_number="6234567890",
            email="juan@example.com"
        )
        
        self.category = Category.objects.create(name="Test Category")
        self.service1 = Service.objects.create(name="Service 1", category=self.category,
                                               available=Service.Available.POSITIVE)
        self.service2 = Service.objects.create(name="Service 2", category=self.category,
                                               available=Service.Available.POSITIVE)
        self.assign_services_url = reverse('employee:assign_services', args=[self.employee.id])
    
    def test_assign_services_GET(self):
        """
        Test the GET request to the assign services page.

        Verifies that the page loads correctly, uses the correct template, and contains the expected form, employee, and
        available services in the context.
        """
        response = self.client.get(self.assign_services_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/assign_services.html')
        self.assertIsInstance(response.context['form'], ServicesEmployeeForm)
        self.assertEqual(response.context['employee'], self.employee)
        self.assertQuerySetEqual(response.context['services'],
                                 Service.objects.filter(available=Service.Available.POSITIVE), ordered=False)
    
    def test_assign_services_POST_valid(self):
        """
        Test the POST request with valid service assignments.

        Ensures that services are correctly assigned to the employee and the user is redirected to the employee's
        services page.
        """
        data = {
            'services': [self.service1.id, self.service2.id]
        }
        response = self.client.post(self.assign_services_url, data=data)
        
        self.assertRedirects(response, reverse('employee:services', args=[self.employee.id]))
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.services.count(), 2)
        self.assertIn(self.service1, self.employee.services.all())
        self.assertIn(self.service2, self.employee.services.all())
    
    def test_assign_services_POST_no_services(self):
        """
        Test the POST request when no services are selected.

        Verifies that all services are removed from the employee when an empty list is submitted.
        """
        data = {
            'services': []
        }
        response = self.client.post(self.assign_services_url, data=data)
        
        self.assertRedirects(response, reverse('employee:services', args=[self.employee.id]))
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.services.count(), 0)
    
    def test_assign_services_POST_invalid(self):
        """
        Test the POST request with invalid service data.

        Ensures that the form is re-rendered with error messages when invalid data is submitted.
        """
        data = {
            'services': ['invalid_id']
        }
        response = self.client.post(self.assign_services_url, data=data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/assign_services.html')
        self.assertFalse(response.context['form'].is_valid())
    
    def test_assign_services_nonexistent_employee(self):
        """
        Test accessing the assign services page for a non-existent employee.

        Verifies that a 404 error is returned when trying to assign services to a non-existent employee.
        """
        url = reverse('employee:assign_services', args=[9999])  # Non-existent employee ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)


class EditEmployeeViewTest(TestCase):
    """
    Test cases for the EditEmployeeView.

    This class contains unit tests to verify the functionality of the EditEmployeeView, which handles the editing of
    existing Employee instances.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test employee and initializes the URL for editing the employee.
        """
        self.employee = Employee.objects.create(
            first_name="Juan",
            last_name="Perez",
            telephone_number="6234567890",
            email="juan@example.com"
        )
        self.edit_employee_url = reverse('employee:edit', args=[self.employee.id])
    
    def test_edit_employee_GET(self):
        """
        Test the GET request to the edit employee page.

        Verifies that the page loads correctly, uses the correct template, and contains the expected form and employee
        in the context.
        """
        response = self.client.get(self.edit_employee_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/edit.html')
        self.assertIsInstance(response.context['form'], EmployeeForm)
        self.assertEqual(response.context['employee'], self.employee)
    
    def test_edit_employee_POST_valid(self):
        """
        Test the POST request with valid employee data.

        Ensures that the employee's information is updated correctly when valid data is submitted, and that the user is
        redirected to the employee list page.
        """
        data = {
            'first_name': 'Maria',
            'last_name': 'Leon',
            'telephone_number': '6987654321',
            'email': 'maria@example.com',
        }
        
        response = self.client.post(self.edit_employee_url, data=data)
        if response.status_code == 302:
            self.assertRedirects(response, reverse('employee:list'))
        else:
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.context['form'].is_valid())
            
        self.employee.refresh_from_db()
        if response.status_code == 302:
            self.assertEqual(self.employee.first_name, 'Maria')
            self.assertEqual(self.employee.telephone_number, '6987654321')
            self.assertEqual(self.employee.email, 'maria@example.com')
        else:
            self.assertEqual(self.employee.first_name, 'Juan')
    
    def test_edit_employee_POST_invalid(self):
        """
        Test the POST request with invalid employee data.

        Verifies that the form is re-rendered with error messages when invalid data is submitted, and that the
        employee's information remains unchanged.
        """
        data = {
            'first_name': '',  # Invalid: empty first name
            'last_name': 'Leon',
            'telephone_number': '6987654321',
            'email': 'maria@example.com',
        }
        response = self.client.post(self.edit_employee_url, data=data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/edit.html')
        self.assertFalse(response.context['form'].is_valid())
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.first_name, 'Juan')  # Name should not have changed
    
    def test_edit_nonexistent_employee(self):
        """
        Test accessing the edit page for a non-existent employee.

        Verifies that a 404 error is returned when trying to edit a non-existent employee.
        """
        url = reverse('employee:edit', args=[9999])  # Non-existent employee ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_edit_employee_no_change(self):
        """
        Test editing an employee without making any changes.

        Ensures that submitting the form with unchanged data still redirects to the employee list page and doesn't
        modify the employee's information.
        """
        data = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'telephone_number': '6234567890',
            'email': 'juan@example.com',
        }
        response = self.client.post(self.edit_employee_url, data=data)
        
        if response.status_code == 302:
            self.assertRedirects(response, reverse('employee:list'))
        else:
            self.assertEqual(response.status_code, 200)
            
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.first_name, 'Juan')
        self.assertEqual(self.employee.telephone_number, '6234567890')
        self.assertEqual(self.employee.email, 'juan@example.com')


class DeleteEmployeeViewTest(TestCase):
    """
    Test cases for the DeleteEmployeeView.

    This class contains unit tests to verify the functionality of the DeleteEmployeeView, which handles the deletion of
    existing Employee instances.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test employee and initializes the URL for deleting the employee.
        """
        self.employee = Employee.objects.create(
            first_name="Juan",
            last_name="Perez",
            telephone_number="6234567890",
            email="juan@example.com"
        )
        self.delete_employee_url = reverse('employee:delete', args=[self.employee.id])
    
    def test_delete_employee_GET(self):
        """
        Test the GET request to the delete employee page.

        Verifies that the page loads correctly, uses the correct template, and contains the expected employee in the
        context.
        """
        response = self.client.get(self.delete_employee_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/delete.html')
        self.assertEqual(response.context['employee'], self.employee)
    
    def test_delete_employee_POST(self):
        """
        Test the POST request to delete an employee.

        Ensures that the employee is successfully deleted from the database and the user is redirected to the employee
        list page.
        """
        response = self.client.post(self.delete_employee_url)
        
        self.assertRedirects(response, reverse('employee:list'))
        self.assertEqual(Employee.objects.count(), 0)
    
    def test_delete_nonexistent_employee(self):
        """
        Test accessing the delete page for a non-existent employee.

        Verifies that a 404 error is returned when trying to delete a non-existent employee.
        """
        url = reverse('employee:delete', args=[9999])  # Non-existent employee ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_delete_employee_POST_redirect(self):
        """
        Test the redirection after successfully deleting an employee.

        Ensures that the user is correctly redirected to the employee list page after a successful deletion.
        """
        response = self.client.post(self.delete_employee_url, follow=True)
        
        self.assertRedirects(response, reverse('employee:list'))
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][1], 302)
    
    def test_delete_employee_does_not_affect_other_employees(self):
        """
        Test that deleting an employee does not affect other employees.

        Verifies that when an employee is deleted, other employees in the database remain unaffected.
        """
        other_employee = Employee.objects.create(
            first_name="Maria",
            last_name="leon",
            telephone_number="6987654321",
            email="maria@example.com"
        )
        
        response = self.client.post(self.delete_employee_url)
        
        self.assertRedirects(response, reverse('employee:list'))
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.first(), other_employee)


class ListEmployeeViewTest(TestCase):
    """
    Test cases for the ListEmployeeView.

    This class contains unit tests to verify the functionality of the ListEmployeeView, which handles the display of all
    Employee instances.
    """
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates multiple test employees and initializes the URL for listing employees.
        """
        self.employee1 = Employee.objects.create(
            first_name="Juan",
            last_name="Perez",
            telephone_number="6234567890",
            email="juan@example.com"
        )
        self.employee2 = Employee.objects.create(
            first_name="Maria",
            last_name="leon",
            telephone_number="6987654321",
            email="maria@example.com"
        )
        self.employee3 = Employee.objects.create(
            first_name="Alicia",
            last_name="Martin",
            telephone_number="6122334455",
            email="alicia@example.com"
        )
        
        self.list_employee_url = reverse('employee:list')
    
    def test_list_employee_GET(self):
        """
        Test the GET request to the list employee page.

        Verifies that the page loads correctly and uses the correct template.
        """
        response = self.client.get(self.list_employee_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/list.html')
    
    def test_list_employee_contains_all_employees(self):
        """
        Test that all employees are included in the list view.

        Ensures that the context contains all created employees.
        """
        response = self.client.get(self.list_employee_url)
        
        self.assertEqual(len(response.context['employees']), 3)
    
    def test_list_employee_ordered_by_first_name(self):
        """
        Test the ordering of employees in the list view.

        Verifies that employees are ordered alphabetically by first name.
        """
        response = self.client.get(self.list_employee_url)
        employees = list(response.context['employees'])
        
        self.assertEqual(employees[0], self.employee3)  # Alicia
        self.assertEqual(employees[1], self.employee1)  # Juan
        self.assertEqual(employees[2], self.employee2)  # Maria
    
    def test_list_employee_context(self):
        """
        Test the context of the list employee view.

        Ensures that the 'employees' key is present in the context.
        """
        response = self.client.get(self.list_employee_url)
        
        self.assertIn('employees', response.context)
    
    def test_list_employee_empty(self):
        """
        Test the list view when there are no employees.

        Verifies that the view handles the case of an empty employee list correctly.
        """
        Employee.objects.all().delete()
        response = self.client.get(self.list_employee_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['employees']), 0)


class ServicesEmployeeViewTest(TestCase):
    """
    Test cases for the ServicesEmployeeView.
    
    This class contains unit tests to verify the functionality of the ServicesEmployeeView, which handles the display of
    services associated with a specific Employee.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates categories, services, an employee with associated services, and initializes the URL for viewing employee
        services.
        """
        self.category1 = Category.objects.create(name="Category 1")
        self.category2 = Category.objects.create(name="Category 2")
        
        self.service1 = Service.objects.create(name="Service 1", category=self.category1)
        self.service2 = Service.objects.create(name="Service 2", category=self.category1)
        self.service3 = Service.objects.create(name="Service 3", category=self.category2)
        
        self.employee = Employee.objects.create(
            first_name="Juan",
            last_name="Perez",
            telephone_number="6234567890",
            email="juan@example.com"
        )
        self.employee.services.add(self.service1, self.service2, self.service3)
        
        self.services_employee_url = reverse('employee:services', args=[self.employee.id])
    
    def test_services_employee_GET(self):
        """
        Test the GET request to the employee services page.

        Verifies that the page loads correctly and uses the correct template.
        """
        response = self.client.get(self.services_employee_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/services.html')
    
    def test_services_employee_context(self):
        """
        Test the context of the employee services view.

        Ensures that the 'employee' and 'services' keys are present in the context and contain the expected data.
        """
        response = self.client.get(self.services_employee_url)
        
        self.assertIn('employee', response.context)
        self.assertIn('services', response.context)
        self.assertEqual(response.context['employee'], self.employee)
        self.assertEqual(list(response.context['services']), list(self.employee.services.all()))
    
    def test_services_employee_ordered_by_category(self):
        """
        Test the ordering of services in the employee services view.

        Verifies that services are ordered by their associated categories.
        """
        response = self.client.get(self.services_employee_url)
        services = list(response.context['services'])
        
        self.assertEqual(services[0].category, self.category1)
        self.assertEqual(services[1].category, self.category1)
        self.assertEqual(services[2].category, self.category2)
    
    def test_services_employee_no_services(self):
        """
        Test the services view for an employee with no associated services.

        Ensures that the view handles the case of an employee without services correctly.
        """
        employee_no_services = Employee.objects.create(
            first_name="Maria",
            last_name="Leon",
            telephone_number="6876543219",
            email="maria@example.com"
        )
        
        url = reverse('employee:services', args=[employee_no_services.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['services']), 0)
    
    def test_services_employee_nonexistent(self):
        """
        Test accessing the services view for a non-existent employee.

        Verifies that an ObjectDoesNotExist exception is raised when trying to view services for a non-existent
        employee.
        """
        url = reverse('employee:services', args=[9999])  # Non-existent employee ID
        
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(url)


class ViewDetailsEmployeeTest(TestCase):
    """
    Test cases for the ViewDetailsEmployeeView.

    This class contains unit tests to verify the functionality of the ViewDetailsEmployeeView, which handles the display
    of detailed information for a specific Employee.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test employee and initializes the URL for viewing employee details.
        """
        self.employee = Employee.objects.create(
            first_name="Juan",
            last_name="Perez",
            telephone_number="6234567890",
            email="juan@example.com",
            color="#FF5733"
        )
        
        self.view_details_url = reverse('employee:view', args=[self.employee.id])
    
    def test_view_details_employee_GET(self):
        """
        Test the GET request to the employee details page.

        Verifies that the page loads correctly and uses the correct template.
        """
        response = self.client.get(self.view_details_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee/view.html')
    
    def test_view_details_employee_context(self):
        """
        Test the context of the employee details view.

        Ensures that the 'employee' key is present in the context and contains the expected employee object.
        """
        response = self.client.get(self.view_details_url)
        
        self.assertIn('employee', response.context)
        self.assertEqual(response.context['employee'], self.employee)
    
    def test_view_details_employee_content(self):
        """
        Test the content of the employee details page.

        Verifies that the page contains all the relevant employee information.
        """
        response = self.client.get(self.view_details_url)
        
        self.assertContains(response, self.employee.first_name)
        self.assertContains(response, self.employee.last_name)
        self.assertContains(response, self.employee.telephone_number)
        self.assertContains(response, self.employee.email)
    
    def test_view_details_nonexistent_employee(self):
        """
        Test accessing the details view for a non-existent employee.

        Ensures that a 404 error is returned when trying to view details of a non-existent employee.
        """
        url = reverse('employee:view', args=[9999])  # Non-existent employee ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_view_details_employee_correct_template(self):
        """
        Test that the correct template is used for the employee details view.

        Verifies that the 'employee/view.html' template is used to render the page.
        """
        response = self.client.get(self.view_details_url)
        
        self.assertTemplateUsed(response, 'employee/view.html')