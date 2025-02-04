from datetime import timedelta

from django.core.paginator import Page
from django.test import TestCase
from django.urls import reverse

from service.models import Service, Category, Voucher
from service.forms import CategoryForm, ServiceForm, VoucherForm


class AddServiceViewTest(TestCase):
    """
    Test cases for the AddServiceView.

    This class contains unit tests to verify the functionality of the AddServiceView, which handles the creation of new
    Service instances.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test category and initializes the URL for adding a service.
        """
        self.category = Category.objects.create(name="Test Category", color="#123456")
        self.add_service_url = reverse('service:service_add')

    def test_add_service_GET(self):
        """
        Test the GET request to the add service page.

        Verifies that the page loads correctly, uses the correct template, and contains the expected form in the
        context.
        """
        response = self.client.get(self.add_service_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service/add.html')
        self.assertIsInstance(response.context['form'], ServiceForm)

    def test_add_service_POST_valid(self):
        """
        Test the POST request with valid service data.

        Ensures that a new service is created with the provided data and that the user is redirected to the category
        list page.
        """
        service_data = {
            'name': 'Test Service',
            'category': self.category.id,
            'price': 50.00,
            'duration': timedelta(hours=1, minutes=30),
            'available': Service.Available.POSITIVE
        }
        response = self.client.post(self.add_service_url, data=service_data)
        
        self.assertRedirects(response, reverse('service:category_list'))
        self.assertEqual(Service.objects.count(), 1)
        
        new_service = Service.objects.first()
        
        self.assertEqual(new_service.name, 'Test Service')
        self.assertEqual(new_service.duration, timedelta(hours=1, minutes=30))

    def test_add_service_POST_invalid(self):
        """
        Test the POST request with invalid service data.

        Verifies that no service is created when invalid data is submitted, and that the form is re-rendered with error
        messages.
        """
        service_data = {
            'name': '',  # Invalid: empty name
            'price': 'not a number',  # Invalid: not a number
            'duration': 'invalid',  # Invalid: wrong format
        }
        
        response = self.client.post(self.add_service_url, data=service_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service/add.html')
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Service.objects.count(), 0)

    def test_add_service_form_in_template(self):
        """
        Test the presence of the service form in the template.

        Ensures that the form and its fields are correctly rendered in the HTML.
        """
        response = self.client.get(self.add_service_url)
        
        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="category"')
        self.assertContains(response, 'name="price"')
        self.assertContains(response, 'name="duration"')
        self.assertContains(response, 'name="available"')
        
        
class EditServiceViewTest(TestCase):
    """
    Test cases for the EditServiceView.

    This class contains unit tests to verify the functionality of the EditServiceView, which handles the editing of
    existing Service instances.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test category and service, and initializes the URL for editing the service.
        """
        self.category = Category.objects.create(name="Test Category", color="#123456")
        self.service = Service.objects.create(
            name="Test Service",
            category=self.category,
            price=50.00,
            duration=timedelta(hours=1),
            available=Service.Available.POSITIVE
        )
        self.edit_service_url = reverse('service:service_edit', args=[self.service.id])

    def test_edit_service_GET(self):
        """
        Test the GET request to the edit service page.

        Verifies that the page loads correctly, uses the correct template, and contains the expected form and service in
        the context.
        """
        response = self.client.get(self.edit_service_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service/edit.html')
        self.assertIsInstance(response.context['form'], ServiceForm)
        self.assertEqual(response.context['service'], self.service)

    def test_edit_service_POST_valid(self):
        """
        Test the POST request with valid updated service data.

        Ensures that the service is updated with the provided data and that the user is redirected to the service view
        page.
        """
        updated_data = {
            'name': 'Updated Service',
            'category': self.category.id,
            'price': 60.00,
            'duration': timedelta(hours=1, minutes=30),
            'available': Service.Available.NEGATIVE
        }
        
        response = self.client.post(self.edit_service_url, data=updated_data)
        
        self.assertRedirects(response, reverse('service:service_view', args=[self.service.id]))
        self.service.refresh_from_db()
        self.assertEqual(self.service.name, 'Updated Service')
        self.assertEqual(self.service.price, 60.00)
        self.assertEqual(self.service.duration, timedelta(hours=1, minutes=30))
        self.assertEqual(self.service.available, Service.Available.NEGATIVE)

    def test_edit_service_POST_invalid(self):
        """
        Test the POST request with invalid service data.

        Verifies that the service is not updated when invalid data is submitted, and that the form is re-rendered with
        error messages.
        """
        invalid_data = {
            'name': '',  # Invalid: empty name
            'price': 'not a number',  # Invalid: not a number
            'duration': 'invalid',  # Invalid: wrong format
        }
        
        response = self.client.post(self.edit_service_url, data=invalid_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service/edit.html')
        self.assertFalse(response.context['form'].is_valid())
        self.service.refresh_from_db()
        self.assertEqual(self.service.name, 'Test Service')  # Name should not have changed

    def test_edit_nonexistent_service(self):
        """
        Test accessing the edit page for a non-existent service.

        Ensures that a 404 error is returned when trying to edit a non-existent service.
        """
        url = reverse('service:service_edit', args=[9999])  # Non-existent service ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)

    def test_edit_service_form_initial_values(self):
        """
        Test the initial values of the edit service form.

        Verifies that the form is pre-populated with the current service data.
        """
        response = self.client.get(self.edit_service_url)
        form = response.context['form']
        
        self.assertEqual(form.initial['name'], 'Test Service')
        self.assertEqual(form.initial['category'], self.category.id)
        self.assertEqual(form.initial['price'], 50.00)
        self.assertEqual(form.initial['duration'], timedelta(hours=1))
        self.assertEqual(form.initial['available'], Service.Available.POSITIVE)
        
        
class DeleteServiceViewTest(TestCase):
    """
    Test cases for the DeleteServiceView.

    This class contains unit tests to verify the functionality of the DeleteServiceView, which handles the deletion of
    existing Service instances.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test category and service, and initializes the URL for deleting the service.
        """
        self.category = Category.objects.create(name="Test Category", color="#123456")
        self.service = Service.objects.create(
            name="Test Service",
            category=self.category,
            price=50.00,
            duration=timedelta(hours=1),
            available=Service.Available.POSITIVE
        )
        self.delete_service_url = reverse('service:service_delete', args=[self.service.id])

    def test_delete_service_GET(self):
        """
        Test the GET request to the delete service page.

        Verifies that the page loads correctly, uses the correct template, and contains the expected service in the
        context.
        """
        response = self.client.get(self.delete_service_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service/delete.html')
        self.assertEqual(response.context['service'], self.service)

    def test_delete_service_POST(self):
        """
        Test the POST request to delete a service.

        Ensures that the service is deleted and the user is redirected to the category list page.
        """
        response = self.client.post(self.delete_service_url)
        
        self.assertRedirects(response, reverse('service:category_list'))
        self.assertEqual(Service.objects.count(), 0)

    def test_delete_nonexistent_service(self):
        """
        Test accessing the delete page for a non-existent service.

        Ensures that a 404 error is returned when trying to delete a non-existent service.
        """
        url = reverse('service:service_delete', args=[9999])  # Non-existent service ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)

    def test_delete_service_POST_redirect(self):
        """
        Test the redirection after successfully deleting a service.

        Verifies that the user is correctly redirected to the category list page after deletion.
        """
        response = self.client.post(self.delete_service_url, follow=True)
        
        self.assertRedirects(response, reverse('service:category_list'))
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][1], 302)

    def test_delete_service_confirmation_page(self):
        """
        Test the content of the delete confirmation page.

        Ensures that the confirmation page contains the correct service name and confirmation message.
        """
        response = self.client.get(self.delete_service_url)
        
        self.assertContains(response,
                            '¿Estás segura de que deseas eliminar el servicio <b>Test Service</b>?')
        self.assertContains(response, self.service.name)

    def test_delete_service_does_not_affect_other_services(self):
        """
        Test that deleting a service does not affect other services.

        Verifies that when a service is deleted, other services in the database remain unaffected.
        """
        other_service = Service.objects.create(
            name="Other Service",
            category=self.category,
            price=75.00,
            duration=timedelta(hours=2),
            available=Service.Available.POSITIVE
        )
        
        response = self.client.post(self.delete_service_url)
        
        self.assertRedirects(response, reverse('service:category_list'))
        self.assertEqual(Service.objects.count(), 1)
        self.assertEqual(Service.objects.first(), other_service)


class ServicesCategoryViewTest(TestCase):
    """
    Test cases for the ServicesCategoryView.

    This class contains unit tests to verify the functionality of the ServicesCategoryView, which handles the display of
    services for a specific category.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test category and multiple services for pagination testing, and initializes the URL for viewing
        services of the category.
        """
        self.category = Category.objects.create(name="Test Category", color="#123456")
        
        # Create 25 services for pagination testing
        for i in range(25):
            Service.objects.create(
                name=f"Test Service {i}",
                category=self.category,
                price=50.00,
                duration=timedelta(hours=1),
                available=Service.Available.POSITIVE
            )
        
        self.services_category_url = reverse('service:service_services_category', args=[self.category.id])
    
    def test_services_category_GET(self):
        """
        Test the GET request to the services category page.

        Verifies that the page loads correctly, uses the correct template, and contains the expected category and
        services in the context.
        """
        response = self.client.get(self.services_category_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service/services_category.html')
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(len(response.context['services']), 20)  # First page should have 20 services
    
    def test_services_category_pagination(self):
        """
        Test the pagination of services in the category view.

        Ensures that the correct number of services are displayed on different pages.
        """
        response = self.client.get(self.services_category_url + '?page=2')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['services']), 5)  # Second page should have 5 services
    
    def test_services_category_invalid_page(self):
        """
        Test the behavior when requesting an invalid page number.

        Verifies that the last available page is returned when requesting a page beyond the available pages.
        """
        response = self.client.get(self.services_category_url + '?page=3')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['services']), 5)  # Should return last page
    
    def test_services_category_non_integer_page(self):
        """
        Test the behavior when requesting a non-integer page number.

        Ensures that the first page is returned when the page parameter is not a valid integer.
        """
        response = self.client.get(self.services_category_url + '?page=abc')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['services']), 20)  # Should return first page
    
    def test_services_category_nonexistent_category(self):
        """
        Test accessing the services page for a non-existent category.

        Ensures that a 404 error is returned when trying to view services of a non-existent category.
        """
        url = reverse('service:service_services_category', args=[9999])  # Non-existent category ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_services_category_empty_category(self):
        """
        Test the display of an empty category.

        Verifies that the page loads correctly for a category with no services.
        """
        empty_category = Category.objects.create(name="Empty Category", color="#654321")
        url = reverse('service:service_services_category', args=[empty_category.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['services']), 0)
    
    def test_services_category_context(self):
        """
        Test the context of the services category view.

        Ensures that the correct keys are present in the context and that the services are paginated.
        """
        response = self.client.get(self.services_category_url)
        
        self.assertIn('category', response.context)
        self.assertIn('services', response.context)
        self.assertIsInstance(response.context['services'], Page)


class ServicesWithoutCategoryViewTest(TestCase):
    """
    Test cases for the ServicesWithoutCategoryView.

    This class contains unit tests to verify the functionality of the ServicesWithoutCategoryView, which handles the
    display of services that are not associated with any category.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test category and multiple services with and without categories, and initializes the URL for viewing
        services without a category.
        """
        self.category = Category.objects.create(name="Test Category", color="#123456")
        
        # Create services with and without category
        self.service_with_category = Service.objects.create(
            name="Service With Category",
            category=self.category,
            price=50.00,
            duration=timedelta(hours=1),
            available=Service.Available.POSITIVE
        )
        self.service_without_category1 = Service.objects.create(
            name="Service Without Category 1",
            price=60.00,
            duration=timedelta(hours=2),
            available=Service.Available.POSITIVE
        )
        self.service_without_category2 = Service.objects.create(
            name="Service Without Category 2",
            price=70.00,
            duration=timedelta(hours=3),
            available=Service.Available.NEGATIVE
        )
        
        self.services_without_category_url = reverse('service:service_services_without_category')
    
    def test_services_without_category_GET(self):
        """
        Test the GET request to the services without category page.

        Verifies that the page loads correctly, uses the correct template, and contains only the services without a
        category in the context.
        """
        response = self.client.get(self.services_without_category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service/services_without_category.html')
        
        services_in_context = response.context['services']
        self.assertEqual(len(services_in_context), 2)
        self.assertIn(self.service_without_category1, services_in_context)
        self.assertIn(self.service_without_category2, services_in_context)
        self.assertNotIn(self.service_with_category, services_in_context)
    
    def test_services_without_category_empty(self):
        """
        Test the behavior when there are no services without a category.

        Ensures that the page loads correctly and displays an empty list when all services have been assigned
        categories.
        """
        # Delete all services without category
        Service.objects.filter(category__isnull=True).delete()
        
        response = self.client.get(self.services_without_category_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['services']), 0)
    
    def test_services_without_category_content(self):
        """
        Test the content of the services without category page.

        Verifies that the page contains the names of services without a category and does not contain the names of
        services with a category.

        """
        response = self.client.get(self.services_without_category_url)
        
        self.assertContains(response, "Service Without Category 1")
        self.assertContains(response, "Service Without Category 2")
        self.assertNotContains(response, "Service With Category")
    
    def test_services_without_category_context(self):
        """
        Test the context of the services without category view.

        Ensures that the 'services' key is present in the context and contains the correct queryset of services without
        a category.
        """
        response = self.client.get(self.services_without_category_url)
        self.assertIn('services', response.context)
        self.assertQuerySetEqual(
            response.context['services'],
            Service.objects.filter(category__isnull=True),
            ordered=False
        )


class ViewDetailsServiceTest(TestCase):
    """
    Test cases for the ViewDetailsServiceView.

    This class contains unit tests to verify the functionality of the ViewDetailsServiceView, which handles the display
    of detailed information for a specific Service.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test category and service, and initializes the URL for viewing service details.
        """
        self.category = Category.objects.create(name="Test Category", color="#123456")
        
        self.service = Service.objects.create(
            name="Test Service",
            category=self.category,
            price=50.00,
            duration=timedelta(hours=1),
            available=Service.Available.POSITIVE
        )
        
        self.view_details_url = reverse('service:service_view', args=[self.service.id])
    
    def test_view_details_service_GET(self):
        """
        Test the GET request to the service details page.

        Verifies that the page loads correctly, uses the correct template, and contains the expected service in the
        context.
        """
        response = self.client.get(self.view_details_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service/view.html')
        self.assertEqual(response.context['service'], self.service)
    
    def test_view_details_service_content(self):
        """
        Test the content of the service details page.

        Ensures that the page contains all relevant service information, including name, category, formatted price,
        duration, and availability.
        """
        response = self.client.get(self.view_details_url)
        self.assertContains(response, self.service.name)
        self.assertContains(response, self.service.category.name)

        # Check for the formatted price
        formatted_price = f"{self.service.price:.2f}€".replace('.', ',')
        self.assertContains(response, formatted_price)
        
        # Check for the formatted duration
        formatted_duration = ':'.join(str(self.service.duration).split(':')[:2])  # Only hours and minutes
        self.assertContains(response, formatted_duration)
        
        # Check for availability (SI or NO)
        availability = "SI" if self.service.available == Service.Available.POSITIVE else "NO"
        self.assertContains(response, availability)
    
    def test_view_details_nonexistent_service(self):
        """
        Test accessing the details page for a non-existent service.

        Ensures that a 404 error is returned when trying to view details of a non-existent service.
        """
        url = reverse('service:service_view', args=[9999])  # Non-existent service ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_view_details_service_context(self):
        """
        Test the context of the service details view.

        Verifies that the 'service' key is present in the context and contains the correct service object.
        """
        response = self.client.get(self.view_details_url)
        
        self.assertIn('service', response.context)
        self.assertEqual(response.context['service'], self.service)
    
    def test_view_details_service_without_category(self):
        """
        Test viewing details of a service without a category.

        Ensures that the page loads correctly for a service without a category and does not display any category
        information.
        """
        service_without_category = Service.objects.create(
            name="Service Without Category",
            price=60.00,
            duration=timedelta(hours=2),
            available=Service.Available.NEGATIVE
        )
        
        url = reverse('service:service_view', args=[service_without_category.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Category")
        
        
class AddCategoryViewTest(TestCase):
    """
    Test cases for the AddCategoryView.

    This class contains unit tests to verify the functionality of the AddCategoryView, which handles the creation of new
    Category instances.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Initializes the URL for adding a category
        """
        self.add_category_url = reverse('service:category_add')

    def test_add_category_GET(self):
        """
        Test the GET request to the add category page.

        Verifies that the page loads correctly, uses the correct template, and contains the expected form in the
        context.
        """
        response = self.client.get(self.add_category_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category/add.html')
        self.assertIsInstance(response.context['form'], CategoryForm)

    def test_add_category_POST_valid(self):
        """
        Test the POST request with valid category data.

        Ensures that a new category is created with the provided data and that the user is redirected to the category
        list page.
        """
        category_data = {
            'name': 'Test Category',
            'color': '#123456'
        }
        
        response = self.client.post(self.add_category_url, data=category_data)
        self.assertRedirects(response, reverse('service:category_list'))
        self.assertEqual(Category.objects.count(), 1)
        
        new_category = Category.objects.first()
        self.assertEqual(new_category.name, 'Test Category')
        self.assertEqual(new_category.color, '#123456')

    def test_add_category_POST_invalid(self):
        """
        Test the POST request with invalid category data.

        Verifies that no category is created when invalid data is submitted, and that the form is re-rendered with error
        messages.
        """
        category_data = {
            'name': '',  # Invalid: empty name
            'color': 'invalid_color'  # Invalid: not a valid color format
        }
        
        response = self.client.post(self.add_category_url, data=category_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category/add.html')
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Category.objects.count(), 0)

    def test_add_category_form_in_template(self):
        """
        Test the presence of the category form in the template.

        Ensures that the form and its fields are correctly rendered in the HTML.
        """
        response = self.client.get(self.add_category_url)
        
        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="color"')
        
        
class EditCategoryViewTest(TestCase):
    """
    Test cases for the EditCategoryView.

    This class contains unit tests to verify the functionality of the EditCategoryView, which handles the editing of
    existing Category instances.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test category and initializes the URL for editing the category.
        """
        self.category = Category.objects.create(name="Test Category", color="#123456")
        self.edit_category_url = reverse('service:category_edit', args=[self.category.id])

    def test_edit_category_GET(self):
        """
        Test the GET request to the edit category page.

        Verifies that the page loads correctly, uses the correct template,and contains the expected form and category in
        the context.
        """
        response = self.client.get(self.edit_category_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category/edit.html')
        self.assertIsInstance(response.context['form'], CategoryForm)
        self.assertEqual(response.context['category'], self.category)

    def test_edit_category_POST_valid(self):
        """
        Test the POST request with valid updated category data.

        Ensures that the category is updated with the provided data and that the user is redirected to the category list
        page.
        """
        updated_data = {
            'name': 'Updated Category',
            'color': '#654321'
        }
        response = self.client.post(self.edit_category_url, data=updated_data)
        self.assertRedirects(response, reverse('service:category_list'))
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')
        self.assertEqual(self.category.color, '#654321')

    def test_edit_category_POST_invalid(self):
        """
        Test the POST request with invalid category data.

        Verifies that the category is not updated when invalid data is submitted, and that the form is re-rendered with
        error messages.
        """
        invalid_data = {
            'name': '',  # Invalid: empty name
            'color': 'invalid_color'  # Invalid: not a valid color format
        }
        response = self.client.post(self.edit_category_url, data=invalid_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category/edit.html')
        self.assertFalse(response.context['form'].is_valid())
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Test Category')  # Name should not have changed

    def test_edit_nonexistent_category(self):
        """
        Test accessing the edit page for a non-existent category.

        Ensures that a 404 error is returned when trying to edit a non-existent category.
        """
        url = reverse('service:category_edit', args=[9999])  # Non-existent category ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)

    def test_edit_category_form_initial_values(self):
        """
        Test the initial values of the edit category form.

        Verifies that the form is pre-populated with the current category data.
        """
        response = self.client.get(self.edit_category_url)
        
        form = response.context['form']
        self.assertEqual(form.initial['name'], 'Test Category')
        self.assertEqual(form.initial['color'], '#123456')
        
        
class DeleteCategoryViewTest(TestCase):
    """
    Test cases for the DeleteCategoryView.

    This class contains unit tests to verify the functionality of the DeleteCategoryView, which handles the deletion of
    existing Category instances.
    """
    
    def setUp(self):
        """
         Set up the test environment before each test method.

        Creates a test category and initializes the URL for deleting the category.
        """
        self.category = Category.objects.create(name="Test Category", color="#123456")
        self.delete_category_url = reverse('service:category_delete', args=[self.category.id])

    def test_delete_category_GET(self):
        """
        Test the GET request to the delete category page.

        Verifies that the page loads correctly, uses the correct template, and contains the expected category in the
        context.
        """
        response = self.client.get(self.delete_category_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category/delete.html')
        self.assertEqual(response.context['category'], self.category)

    def test_delete_category_POST(self):
        """
        Test the POST request to delete a category.

        Ensures that the category is successfully deleted from the database and the user is redirected to the category
        list page.
        """
        response = self.client.post(self.delete_category_url)
        
        self.assertRedirects(response, reverse('service:category_list'))
        self.assertEqual(Category.objects.count(), 0)

    def test_delete_nonexistent_category(self):
        """
        Test accessing the delete page for a non-existent category.

        Ensures that a 404 error is returned when trying to delete a non-existent category.
        """
        url = reverse('service:category_delete', args=[9999])  # Non-existent category ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)

    def test_delete_category_with_services(self):
        """
        Test deleting a category that has associated services.

        Verifies that the category is deleted and its associated services are updated to have no category.
        """
        Service.objects.create(name="Test Service", category=self.category)
        
        response = self.client.post(self.delete_category_url)
        
        self.assertRedirects(response, reverse('service:category_list'))
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(Service.objects.filter(category__isnull=True).count(), 1)

    def test_delete_category_confirmation_page(self):
        """
        Test the content of the delete confirmation page.

        Ensures that the confirmation page contains the correct category name and confirmation message.
        """
        response = self.client.get(self.delete_category_url)
        
        self.assertContains(response,
                            '¿Estás segura de que deseas eliminar la categoría <b>Test Category</b>?')
        self.assertContains(response, self.category.name)


class ListCategoryViewTest(TestCase):
    """
    Test cases for the ListCategoryView.

    This class contains unit tests to verify the functionality of the ListCategoryView, which handles the display of all
    Category instances and Services without a category.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates test categories and services, and initializes the URL for listing categories.
        """
        self.list_category_url = reverse('service:category_list')
        
        # Create some test categories
        self.category1 = Category.objects.create(name="Category 1", color="#123456")
        self.category2 = Category.objects.create(name="Category 2", color="#654321")
        
        # Create some test services
        self.service_with_category = Service.objects.create(name="Service with Category", category=self.category1)
        self.service_without_category = Service.objects.create(name="Service without Category")
    
    def test_list_category_GET(self):
        """
        Test the GET request to the list category page.

        Verifies that the page loads correctly and uses the correct template.
        """
        response = self.client.get(self.list_category_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category/list.html')
    
    def test_list_category_context(self):
        """
        Test the context of the list category view.

        Ensures that the 'categories' and 'services_without_category' keys are present in the context and contain the
        expected querysets.
        """
        response = self.client.get(self.list_category_url)
        
        self.assertIn('categories', response.context)
        self.assertIn('services_without_category', response.context)
        
        # Check if all categories are in the context
        self.assertEqual(list(response.context['categories']), list(Category.objects.all().order_by('name')))
        
        # Check if services without category are in the context
        self.assertEqual(list(response.context['services_without_category']),
                         list(Service.objects.filter(category__isnull=True)))
    
    def test_list_category_content(self):
        """
        Test the content of the list category page.

        Verifies that the page contains the names of all categories and the "Sin categoría" section, but does not
        display individual service names.
        """
        response = self.client.get(self.list_category_url)
        
        self.assertContains(response, "Category 1")
        self.assertContains(response, "Category 2")
        self.assertContains(response, "Sin categoría")
        self.assertNotContains(response, "Service with Category")
    
    def test_list_category_ordering(self):
        """
        Test the ordering of categories in the list view.

        Ensures that categories are ordered alphabetically by name.
        """
        response = self.client.get(self.list_category_url)
        categories = list(response.context['categories'])
        
        self.assertEqual(categories[0].name, "Category 1")
        self.assertEqual(categories[1].name, "Category 2")
    
    def test_list_category_empty(self):
        """
        Test the list view when there are no categories or services.

        Verifies that the view handles the case of empty query sets correctly.
        """
        Category.objects.all().delete()
        Service.objects.all().delete()
        
        response = self.client.get(self.list_category_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['categories']), 0)
        self.assertEqual(len(response.context['services_without_category']), 0)


# Tests voucher views
class AddVoucherViewTest(TestCase):
    """
    Test cases for the AddVoucherView.

    This class contains unit tests to verify the functionality of the AddVoucherView, which handles the creation of new
    Voucher instances.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates test categories and services, and initializes the URL for adding a voucher.
        """
        self.add_voucher_url = reverse('service:voucher_add')
        
        # Create test categories and services
        self.category1 = Category.objects.create(name="Category 1", color="#123456")
        self.category2 = Category.objects.create(name="Category 2", color="#654321")
        self.service1 = Service.objects.create(name="Service 1", category=self.category1, price=50)
        self.service2 = Service.objects.create(name="Service 2", category=self.category2, price=75)
        self.service_no_category = Service.objects.create(name="Sin categoría", price=100)
    
    def test_add_voucher_GET(self):
        """
        Test the GET request to the add voucher page.

        Verifies that the page loads correctly, uses the correct template, and contains the expected form and
        services_by_category in the context.
        """
        response = self.client.get(self.add_voucher_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voucher/add.html')
        self.assertIsInstance(response.context['form'], VoucherForm)
        self.assertIn('services_by_category', response.context)
    
    def test_add_voucher_POST_valid(self):
        """
        Test the POST request with valid voucher data.

        Ensures that a new voucher is created with the provided data and that the user is redirected to the voucher list
        page.
        """
        voucher_data = {
            'name': 'Test Voucher',
            'services': [self.service1.id, self.service2.id],
            'price_session': 100,
            'total_sessions': 5,
            'discount': 10
        }
        
        response = self.client.post(self.add_voucher_url, data=voucher_data)
        
        self.assertRedirects(response, reverse('service:voucher_list'))
        self.assertEqual(Voucher.objects.count(), 1)
        
        new_voucher = Voucher.objects.first()
        self.assertEqual(new_voucher.name, 'Test Voucher')
        self.assertEqual(new_voucher.services.count(), 2)
    
    def test_add_voucher_POST_invalid(self):
        """
        Test the POST request with invalid voucher data.

        Verifies that no voucher is created when invalid data is submitted, and that the form is re-rendered with error
        messages.
        """
        voucher_data = {
            'name': '',  # Invalid: empty name
            'price_session': 'not a number',  # Invalid: not a number
            'total_sessions': 0,  # Invalid: should be greater than 0
            'discount': 101  # Invalid: should be between 0 and 100
        }
        
        response = self.client.post(self.add_voucher_url, data=voucher_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voucher/add.html')
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Voucher.objects.count(), 0)
    
    def test_services_by_category_in_context(self):
        """
        Test the services_by_category context variable.

        Ensures that services are correctly grouped by category in the context, including services without a category.
        """
        response = self.client.get(self.add_voucher_url)
        
        services_by_category = response.context['services_by_category']
        
        self.assertEqual(len(services_by_category), 3)  # 2 categories + 1 None for no category
        # Check services without category (first in the list)
        self.assertIsNone(services_by_category[0]['category'])
        self.assertEqual(len(services_by_category[0]['services']), 1)
        self.assertEqual(services_by_category[0]['services'][0].name, "Sin categoría")
        # Check Category 1
        self.assertEqual(services_by_category[1]['category'], self.category1)
        self.assertEqual(len(services_by_category[1]['services']), 1)  # One service without category
        self.assertEqual(services_by_category[1]['services'][0].name, "Service 1")
        # Check Category 2
        self.assertEqual(services_by_category[2]['category'], self.category2)
        self.assertEqual(len(services_by_category[2]['services']), 1)  # One service without category
        self.assertEqual(services_by_category[2]['services'][0].name, "Service 2")
    
    def test_add_voucher_form_in_template(self):
        """
        Test the presence of the voucher form in the template.

        Ensures that the form and its fields are correctly rendered in the HTML.
        """
        response = self.client.get(self.add_voucher_url)
        
        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="services"')
        self.assertContains(response, 'name="price_session"')
        self.assertContains(response, 'name="total_sessions"')
        self.assertContains(response, 'name="discount"')


class DeleteVoucherViewTest(TestCase):
    """
    Test cases for the DeleteVoucherView.

    This class contains unit tests to verify the functionality of the DeleteVoucherView, which handles the deletion of
    existing Voucher instances.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test category, service, and voucher, and initializes the URL for deleting the voucher.
        """
        # Create a test category and service
        self.category = Category.objects.create(name="Test Category", color="#123456")
        self.service = Service.objects.create(name="Test Service", category=self.category, price=50)
        
        # Create a test voucher
        self.voucher = Voucher.objects.create(
            name="Test Voucher",
            price_session=100,
            total_sessions=5,
            discount=10
        )
        self.voucher.services.add(self.service)
        
        self.delete_voucher_url = reverse('service:voucher_delete', args=[self.voucher.id])
    
    def test_delete_voucher_GET(self):
        """
        Test the GET request to the delete voucher page.

        Verifies that the page loads correctly, uses the correct template, and contains the expected voucher in the
        context.
        """
        response = self.client.get(self.delete_voucher_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voucher/delete.html')
        self.assertEqual(response.context['voucher'], self.voucher)
    
    def test_delete_voucher_POST(self):
        """
        Test the POST request to delete a voucher.

        Ensures that the voucher is successfully deleted from the database and the user is redirected to the voucher
        list page.
        """
        response = self.client.post(self.delete_voucher_url)
        
        self.assertRedirects(response, reverse('service:voucher_list'))
        self.assertEqual(Voucher.objects.count(), 0)
    
    def test_delete_nonexistent_voucher(self):
        """
         Test accessing the delete page for a non-existent voucher.

        Ensures that a 404 error is returned when trying to delete a non-existent voucher.
        """
        url = reverse('service:voucher_delete', args=[9999])  # Non-existent voucher ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_delete_voucher_POST_redirect(self):
        """
        Test the redirection after successfully deleting a voucher.

        Verifies that the user is correctly redirected to the voucher list page after deletion.
        """
        response = self.client.post(self.delete_voucher_url, follow=True)
        
        self.assertRedirects(response, reverse('service:voucher_list'))
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][1], 302)
    
    def test_delete_voucher_confirmation_page(self):
        """
        Test the content of the delete confirmation page.

        Ensures that the confirmation page contains the correct voucher name and confirmation message.
        """
        response = self.client.get(self.delete_voucher_url)
        
        self.assertContains(response, '¿Estás segura de que deseas eliminar el bono <b>Test Voucher</b>?')
        self.assertContains(response, self.voucher.name)
    
    def test_delete_voucher_does_not_affect_services(self):
        """
        Test that deleting a voucher does not affect associated services.

        Verifies that when a voucher is deleted, its associated services remain in the database.
        """
        service_count = Service.objects.count()
        
        self.client.post(self.delete_voucher_url)
        self.assertEqual(Service.objects.count(), service_count)
        self.assertTrue(Service.objects.filter(id=self.service.id).exists())


class DetailsVoucherViewTest(TestCase):
    """
    Test cases for the DetailsVoucherView.

    This class contains unit tests to verify the functionality of the DetailsVoucherView, which handles the display of
    detailed information for a specific Voucher.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test category, service, and voucher, and initializes the URL for viewing voucher details.
        """
        # Create a test category and service
        self.category = Category.objects.create(name="Test Category", color="#123456")
        self.service = Service.objects.create(name="Test Service", category=self.category, price=50)
        
        # Create a test voucher
        self.voucher = Voucher.objects.create(
            name="Test Voucher",
            price_session=100,
            total_sessions=5,
            discount=10
        )
        self.voucher.services.add(self.service)
        
        self.details_voucher_url = reverse('service:voucher_details', args=[self.voucher.id])
    
    def test_details_voucher_GET(self):
        """
        Test the GET request to the voucher details page.

        Verifies that the page loads correctly, uses the correct template, and contains the expected voucher in the
        context.
        """
        response = self.client.get(self.details_voucher_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voucher/details.html')
        self.assertEqual(response.context['voucher'], self.voucher)
    
    def test_details_nonexistent_voucher(self):
        """
        Test accessing the details page for a non-existent voucher.

        Ensures that a 404 error is returned when trying to view details of a non-existent voucher.
        """
        url = reverse('service:voucher_details', args=[9999])  # Non-existent voucher ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_details_voucher_content(self):
        """
        Test the content of the voucher details page.

        Ensures that the page contains all relevant voucher information, including name, price per session, total
        sessions, and discount.
        """
        response = self.client.get(self.details_voucher_url)
        
        self.assertContains(response, self.voucher.name)
        self.assertContains(response, str(self.voucher.price_session))
        self.assertContains(response, str(self.voucher.total_sessions))
        self.assertContains(response, str(self.voucher.discount))
    
    def test_details_voucher_associated_services(self):
        """
        Test the display of associated services on the voucher details page.

        Verifies that the page shows the names of services associated with the voucher.
        """
        response = self.client.get(self.details_voucher_url)
        
        self.assertContains(response, self.service.name)
    
    def test_details_voucher_context(self):
        """
        Test the context of the voucher details view.

        Ensures that the 'voucher' key is present in the context and contains the correct voucher object with all its
        attributes.
        """
        response = self.client.get(self.details_voucher_url)
        
        self.assertIn('voucher', response.context)
        voucher_in_context = response.context['voucher']
        self.assertEqual(voucher_in_context.id, self.voucher.id)
        self.assertEqual(voucher_in_context.name, self.voucher.name)
        self.assertEqual(voucher_in_context.price_session, self.voucher.price_session)
        self.assertEqual(voucher_in_context.total_sessions, self.voucher.total_sessions)
        self.assertEqual(voucher_in_context.discount, self.voucher.discount)


class EditVoucherViewTest(TestCase):
    """
    Test cases for the EditVoucherView.

    This class contains unit tests to verify the functionality of the EditVoucherView, which handles the editing of
    existing Voucher instances.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates test categories, services, and a voucher, and initializes the URL for editing the voucher.
        """
        # Create test categories and services
        self.category1 = Category.objects.create(name="Category 1", color="#123456")
        self.category2 = Category.objects.create(name="Category 2", color="#654321")
        self.service1 = Service.objects.create(name="Service 1", category=self.category1, price=50)
        self.service2 = Service.objects.create(name="Service 2", category=self.category2, price=75)
        
        # Create a test voucher
        self.voucher = Voucher.objects.create(
            name="Test Voucher",
            price_session=100,
            total_sessions=5,
            discount=10
        )
        self.voucher.services.add(self.service1)
        
        self.edit_voucher_url = reverse('service:voucher_edit', args=[self.voucher.id])
    
    def test_edit_voucher_GET(self):
        """
        Test the GET request to the edit voucher page.

        Verifies that the page loads correctly, uses the correct template, and contains the expected form, voucher, and
        services_by_category in the context.
        """
        response = self.client.get(self.edit_voucher_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voucher/edit.html')
        self.assertIsInstance(response.context['form'], VoucherForm)
        self.assertEqual(response.context['voucher'], self.voucher)
        self.assertIn('services_by_category', response.context)
    
    def test_edit_voucher_POST_valid(self):
        """
         Test the POST request with valid updated voucher data.

        Ensures that the voucher is updated with the provided data and that the user is redirected to the voucher
        details page.
        """
        updated_data = {
            'name': 'Updated Voucher',
            'services': [self.service1.id, self.service2.id],
            'price_session': 120,
            'total_sessions': 6,
            'discount': 15
        }
        
        response = self.client.post(self.edit_voucher_url, data=updated_data)
        
        self.assertRedirects(response, reverse('service:voucher_details', args=[self.voucher.id]))
        
        # Refresh the voucher from the database
        self.voucher.refresh_from_db()
        self.assertEqual(self.voucher.name, 'Updated Voucher')
        self.assertEqual(self.voucher.price_session, 120)
        self.assertEqual(self.voucher.total_sessions, 6)
        self.assertEqual(self.voucher.discount, 15)
        self.assertEqual(set(self.voucher.services.all()), set([self.service1, self.service2]))
    
    def test_edit_voucher_POST_invalid(self):
        """
        Test the POST request with invalid voucher data.

        Verifies that the voucher is not updated when invalid data is submitted, and that the form is re-rendered with
        error messages.
        """
        invalid_data = {
            'name': '',  # Invalid: empty name
            'price_session': 'not a number',  # Invalid: not a number
            'total_sessions': 0,  # Invalid: should be greater than 0
            'discount': 101  # Invalid: should be between 0 and 100
        }
        response = self.client.post(self.edit_voucher_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voucher/edit.html')
        self.assertFalse(response.context['form'].is_valid())
    
    def test_edit_nonexistent_voucher(self):
        """
        Test accessing the edit page for a non-existent voucher.
        
        Ensures that a 404 error is returned when trying to edit a non-existent voucher.
        """
        url = reverse('service:voucher_edit', args=[9999])  # Non-existent voucher ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_edit_voucher_form_initial_values(self):
        """
        Test the initial values of the edit voucher form.

        Verifies that the form is pre-populated with the current voucher data.
        """
        response = self.client.get(self.edit_voucher_url)
        
        form = response.context['form']
        self.assertEqual(form.initial['name'], 'Test Voucher')
        self.assertEqual(form.initial['price_session'], 100)
        self.assertEqual(form.initial['total_sessions'], 5)
        self.assertEqual(form.initial['discount'], 10)
        self.assertEqual(list(form.fields['services'].initial), list(self.voucher.services.all()))
    
    def test_services_by_category_in_context(self):
        """
         Test the services_by_category context variable.

        Ensures that services are correctly grouped by category in the context.
        """
        response = self.client.get(self.edit_voucher_url)
        
        services_by_category = response.context['services_by_category']
        self.assertEqual(len(services_by_category), 2)
        self.assertEqual(services_by_category[0]['category'], self.category1)
        self.assertEqual(services_by_category[1]['category'], self.category2)
        
        
class VoucherListViewTest(TestCase):
    """
    Test cases for the VoucherListView.

    This class contains unit tests to verify the functionality of the VoucherListView, which handles the display of all
    Voucher instances with pagination.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test category, service, and multiple vouchers for pagination testing, and initializes the URL for
        listing vouchers.
        """
        self.voucher_list_url = reverse('service:voucher_list')

        # Create test category and service
        self.category = Category.objects.create(name="Test Category", color="#123456")
        self.service = Service.objects.create(name="Test Service", category=self.category, price=50)

        # Create 25 test vouchers
        for i in range(25):
            voucher = Voucher.objects.create(
                name=f"Test Voucher {i}",
                price_session=100,
                total_sessions=5,
                discount=10
            )
            voucher.services.add(self.service)

    def test_voucher_list_GET(self):
        """
        Test the GET request to the voucher list page.

        Verifies that the page loads correctly and uses the correct template.
        """
        response = self.client.get(self.voucher_list_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voucher/list.html')

    def test_voucher_list_pagination(self):
        """
        Test the pagination of the voucher list.

        Ensures that the first page contains the correct number of vouchers and that the pagination is working as
        expected.
        """
        response = self.client.get(self.voucher_list_url)
        
        self.assertTrue('vouchers' in response.context)
        self.assertTrue(isinstance(response.context['vouchers'], Page))
        self.assertEqual(len(response.context['vouchers']), 20)  # First page should have 20 vouchers

    def test_voucher_list_second_page(self):
        """
        Test the second page of the voucher list.

        Verifies that the second page loads correctly and contains the expected number of vouchers.
        """
        response = self.client.get(f"{self.voucher_list_url}?page=2")
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('vouchers' in response.context)
        self.assertEqual(len(response.context['vouchers']), 5)  # Second page should have 5 vouchers

    def test_voucher_list_invalid_page(self):
        """
        Test the behavior when requesting an invalid page number.

        Ensures that the last available page is returned when requesting a page beyond the available pages.
        """
        response = self.client.get(f"{self.voucher_list_url}?page=3")
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('vouchers' in response.context)
        self.assertEqual(len(response.context['vouchers']), 5)  # Should return last page (5 vouchers)

    def test_voucher_list_non_integer_page(self):
        """
        Test the behavior when requesting a non-integer page number.

        Verifies that the first page is returned when the page parameter is not a valid integer.
        """
        response = self.client.get(f"{self.voucher_list_url}?page=abc")
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('vouchers' in response.context)
        self.assertEqual(len(response.context['vouchers']), 20)  # Should return first page (20 vouchers)

    def test_voucher_list_ordering(self):
        """
        Test the ordering of vouchers in the list view.

        Ensures that vouchers are ordered alphabetically by name.
        """
        response = self.client.get(self.voucher_list_url)
        
        vouchers = list(response.context['vouchers'])
        self.assertTrue(all(vouchers[i].name <= vouchers[i+1].name for i in range(len(vouchers)-1)))

    def test_voucher_list_content(self):
        """
        Test the content of the voucher list page.

        Verifies that the page contains the correct information for each voucher, including name, formatted price, total
        sessions, and discount.
        """
        response = self.client.get(self.voucher_list_url)
        
        for voucher in response.context['vouchers']:
            self.assertContains(response, voucher.name)
            # Check for the formatted price
            formatted_price = f"{self.service.price:.2f}€".replace('.', ',')
            self.assertContains(response, formatted_price)
            self.assertContains(response, str(voucher.total_sessions))
            self.assertContains(response, str(voucher.discount))


class SearchItemsViewTest(TestCase):
    """
    Test cases for the SearchItemsView.

    This class contains unit tests to verify the functionality of the SearchItemsView, which handles the search functionality for Services and Vouchers.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates test categories, services, and vouchers, and initializes the URLs for searching.
        """
        # Create test category
        self.category = Category.objects.create(name="Test Category", color="#123456")
        
        # Create test services
        self.service1 = Service.objects.create(name="Test Service", category=self.category, price=50)
        self.service2 = Service.objects.create(name="Another Service", category=self.category, price=75)
        
        # Create test vouchers
        self.voucher1 = Voucher.objects.create(name="Test Voucher", price_session=100, total_sessions=5, discount=10)
        self.voucher2 = Voucher.objects.create(name="Another Voucher", price_session=120, total_sessions=6, discount=15)
        
        self.search_service_url = reverse('service:service_search_items', args=['service'])
        self.search_voucher_url = reverse('service:service_search_items', args=['voucher'])
    
    def test_search_service_with_query(self):
        """
        Test searching for services with a specific query.

        Verifies that the search returns the correct service and excludes others.
        """
        response = self.client.get(f"{self.search_service_url}?query=Test")
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shared/search_items.html')
        self.assertContains(response, "Test Service")
        self.assertNotContains(response, "Another Service")
    
    def test_search_voucher_with_query(self):
        """
        Test searching for vouchers with a specific query.

        Verifies that the search returns the correct voucher and excludes others.
        """
        response = self.client.get(f"{self.search_voucher_url}?query=Test")
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shared/search_items.html')
        self.assertContains(response, "Test Voucher")
        self.assertNotContains(response, "Another Voucher")
    
    def test_search_service_empty_query(self):
        """
        Test searching for services with an empty query.

        Ensures that no services are returned for an empty search query.
        """
        response = self.client.get(f"{self.search_service_url}?query=")
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shared/search_items.html')
        self.assertNotContains(response, "Test Service")
        self.assertNotContains(response, "Another Service")
    
    def test_search_voucher_empty_query(self):
        """
        Test searching for vouchers with an empty query.

        Ensures that no vouchers are returned for an empty search query.
        """
        response = self.client.get(f"{self.search_voucher_url}?query=")
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shared/search_items.html')
        self.assertNotContains(response, "Test Voucher")
        self.assertNotContains(response, "Another Voucher")
    
    def test_search_service_case_insensitive(self):
        """
        Test case-insensitive search for services.

        Verifies that the search is case-insensitive for service names.
        """
        response = self.client.get(f"{self.search_service_url}?query=test")
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Service")
    
    def test_search_voucher_case_insensitive(self):
        """
        Test case-insensitive search for vouchers.

        Verifies that the search is case-insensitive for voucher names.
        """
        response = self.client.get(f"{self.search_voucher_url}?query=test")
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Voucher")
    
    def test_search_service_partial_match(self):
        """
        Test partial matching for service search.

        Ensures that services are returned for partial name matches.
        """
        response = self.client.get(f"{self.search_service_url}?query=Serv")
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Service")
        self.assertContains(response, "Another Service")
    
    def test_search_voucher_partial_match(self):
        """
        Test partial matching for voucher search.

        Ensures that vouchers are returned for partial name matches.
        """
        response = self.client.get(f"{self.search_voucher_url}?query=Vouch")
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Voucher")
        self.assertContains(response, "Another Voucher")
    
    def test_search_invalid_model(self):
        """
        Test searching with an invalid model type.

        Verifies that an empty result set is returned for an invalid model type.
        """
        invalid_url = reverse('service:service_search_items', args=['invalid_model'])
        response = self.client.get(f"{invalid_url}?query=Test")
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shared/search_items.html')
        self.assertQuerySetEqual(response.context['items'], [])
        
        
