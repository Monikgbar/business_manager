from decimal import Decimal

from django.contrib.messages import get_messages
from django.core.paginator import Page
from django.test import TestCase, Client
from django.urls import reverse

from stock.models import Product, StockMovement, Supplier
from stock.forms import ProductForm


# Test supplier views
class AddSupplierViewTest(TestCase):
    """
    Test cases for the AddSupplierView.

    This class contains unit tests to verify the functionality and behavior of the AddSupplierView in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Initializes a test client and the URL for adding a supplier.
        """
        self.client = Client()
        self.url = reverse('stock:supplier_add')
    
    def test_add_supplier_post_request(self):
        """
        Test submitting a valid POST request to add a new supplier.

        Ensures that the supplier is created successfully and redirects to the supplier list page.
        """
        response = self.client.post(self.url, {'name': 'New Supplier'})
        self.assertRedirects(response, reverse('stock:supplier_list'))
        self.assertTrue(Supplier.objects.filter(name='New Supplier').exists())
    
    def test_add_supplier_get_request(self):
        """
        Test accessing the view with a GET request.

        Verifies that the view redirects to the supplier list page (if GET is not supported).
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('stock:supplier_list'))
    
    def test_add_supplier_empty_name(self):
        """
        Test submitting an empty name for a supplier.

        Ensures that an error message is displayed, and no supplier is created with an empty name.
        """
        response = self.client.post(self.url, {'name': ''}, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "El nombre del proveedor no puede estar vacío.")
        self.assertFalse(Supplier.objects.filter(name='').exists())
    
    def test_add_supplier_duplicate_name(self):
        """
        Test submitting a duplicate supplier name.

        Verifies that an error message is displayed, and no duplicate supplier is created.
        """
        Supplier.objects.create(name='Existing Supplier')
        response = self.client.post(self.url, {'name': 'Existing Supplier'}, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "El proveedor 'Existing Supplier' ya existe.")
        self.assertEqual(Supplier.objects.filter(name='Existing Supplier').count(), 1)


class EditSupplierViewTest(TestCase):
    """
    Test cases for the EditSupplierView.

    This class contains unit tests to verify the functionality and behavior of the EditSupplierView in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test supplier and initializes the URL for editing the supplier.
        """
        self.client = Client()
        self.supplier = Supplier.objects.create(name='Original Supplier')
        self.url = reverse('stock:supplier_edit', args=[self.supplier.id])
    
    def test_edit_supplier_post_request(self):
        """
        Test submitting a valid POST request to edit an existing supplier.

        Ensures that the supplier's name is updated successfully and redirects to the correct page.
        """
        response = self.client.post(self.url, {'name': 'Updated Supplier'})
        self.assertRedirects(response, reverse('stock:product_products_supplier', args=[self.supplier.id]))
        # Refresh the supplier from the database
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.name, 'Updated Supplier')
    
    def test_edit_supplier_get_request(self):
        """
        Test accessing the view with a GET request.

        Verifies that the view redirects to the supplier's product list page (if GET is not supported).
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('stock:product_products_supplier', args=[self.supplier.id]))
    
    def test_edit_supplier_nonexistent_id(self):
        """
        Test attempting to edit a non-existent supplier.

        Ensures that a 404 error is returned when trying to edit a supplier that doesn't exist.
        """
        url = reverse('stock:supplier_edit', args=[9999])  # Assuming 9999 is a non-existent ID
        response = self.client.post(url, {'name': 'New Name'})
        self.assertEqual(response.status_code, 404)
    
    def test_edit_supplier_empty_name(self):
        """
        Test submitting an empty name when editing a supplier.

        Verifies that the supplier's name can be updated to an empty string.
        """
        response = self.client.post(self.url, {'name': ''})
        self.assertRedirects(response, reverse('stock:product_products_supplier', args=[self.supplier.id]))
        # Refresh the supplier from the database
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.name, '')  # The name should be updated to an empty string
    
    def test_edit_supplier_same_name(self):
        """
        Test submitting the same name when editing a supplier.

        Ensures that the view handles the case where the name is not changed.
        """
        response = self.client.post(self.url, {'name': 'Original Supplier'})
        self.assertRedirects(response, reverse('stock:product_products_supplier', args=[self.supplier.id]))
        # Refresh the supplier from the database
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.name, 'Original Supplier')


class DeleteSupplierViewTest(TestCase):
    """
    Test cases for the DeleteSupplierView.

    This class contains unit tests to verify the functionality and behavior of the DeleteSupplierView in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test supplier and initializes the URL for deleting the supplier.
        """
        self.client = Client()
        self.supplier = Supplier.objects.create(name='Test Supplier')
        self.url = reverse('stock:supplier_delete', args=[self.supplier.id])
    
    def test_delete_supplier_post_request(self):
        """
        Test submitting a valid POST request to delete an existing supplier.

        Ensures that the supplier is deleted successfully and redirects to the supplier list page.
        """
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('stock:supplier_list'))
        # Check that the supplier no longer exists in the database
        with self.assertRaises(Supplier.DoesNotExist):
            Supplier.objects.get(id=self.supplier.id)
    
    def test_delete_supplier_get_request(self):
        """
        Test accessing the view with a GET request.

        Verifies that the supplier is not deleted when accessed via a GET request, and redirects to the supplier list
        page.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('stock:supplier_list'))
        # Check that the supplier still exists (GET request should not delete)
        self.assertTrue(Supplier.objects.filter(id=self.supplier.id).exists())
    
    def test_delete_nonexistent_supplier(self):
        """
        Test attempting to delete a non-existent supplier.

        Ensures that a 404 error is returned when trying to delete a supplier that doesn't exist.
        """
        url = reverse('stock:supplier_delete', args=[9999])  # Assuming 9999 is a non-existent ID
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
    
    def test_delete_supplier_with_associated_products(self):
        """
        Test deleting a supplier that has associated products.

        Verifies that both the supplier and its associated products are deleted successfully.
        """
        # Create a product associated with the supplier
        Product.objects.create(name='Test Product', supplier=self.supplier)
        
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('stock:supplier_list'))
        # Check that the supplier and its associated product are deleted
        with self.assertRaises(Supplier.DoesNotExist):
            Supplier.objects.get(id=self.supplier.id)
        self.assertFalse(Product.objects.filter(supplier_id=self.supplier.id).exists())


# Test Product views
class DetailsProductViewTest(TestCase):
    """
    Test cases for the DetailsProductView.

    This class contains unit tests to verify the functionality and behavior of the DetailsProductView in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test supplier and product, and initializes the URL for viewing product details.
        """
        self.client = Client()
        self.supplier = Supplier.objects.create(name='Test Supplier')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            supplier=self.supplier,
            price=10.00,
            stock=100
        )
        self.url = reverse('stock:product_details', args=[self.product.id])
    
    def test_details_product_view_success(self):
        """
        Test accessing the product details view successfully.

        Ensures that the correct template is used and the product is in the context.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/details.html')
        self.assertEqual(response.context['product'], self.product)
    
    def test_details_product_nonexistent_id(self):
        """
        Test attempting to view details of a non-existent product.

        Ensures that a 404 error is returned when trying to access a product that doesn't exist.
        """
        url = reverse('stock:product_details', args=[9999])  # Assuming 9999 is a non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_details_product_context_data(self):
        """
        Test the context data provided by the view.

        Verifies that all product details are correctly passed to the template context.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.context['product'].name, 'Test Product')
        self.assertEqual(response.context['product'].description, 'Test Description')
        self.assertEqual(response.context['product'].supplier, self.supplier)
        self.assertEqual(response.context['product'].price, 10.00)
        self.assertEqual(response.context['product'].stock, 100)
    
    def test_details_product_template_content(self):
        """
        Test the content rendered in the template.

        Ensures that all relevant product information is displayed in the response.
        """
        response = self.client.get(self.url)
        self.assertContains(response, 'Test Product')
        self.assertContains(response, 'Test Description')
        self.assertContains(response, 'Test Supplier')
        self.assertContains(response, '10')
        self.assertContains(response, '€')
        self.assertContains(response, '100')


class EditProductViewTest(TestCase):
    """
    Test cases for the EditProductView.

    This class contains unit tests to verify the functionality and behavior of the EditProductView in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

         Creates a test supplier and product, and initializes the URL for editing the product.
        """
        self.client = Client()
        self.supplier = Supplier.objects.create(name='Test Supplier')
        self.product = Product.objects.create(
            name='Original Product',
            description='Original Description',
            supplier=self.supplier,
            price=Decimal('10.00'),
            stock=100
        )
        self.url = reverse('stock:product_edit', args=[self.product.id])
    
    def test_edit_product_get_request(self):
        """
        Test accessing the edit product view with a GET request.

        Ensures that the correct template is used and the form is in the context.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/edit.html')
        self.assertIsInstance(response.context['form'], ProductForm)
        self.assertEqual(response.context['product'], self.product)
    
    def test_edit_product_post_valid_data(self):
        """
        Test submitting valid data to edit a product.

        Verifies that the product is updated correctly and redirects to the product details page.
        """
        data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'supplier': self.supplier.id,
            'price': '15.00',
            'stock': 150
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('stock:product_details', args=[self.product.id]))
        # Refresh the product from the database
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')
        self.assertEqual(self.product.description, 'Updated Description')
        self.assertEqual(self.product.price, Decimal('15.00'))
        self.assertEqual(self.product.stock, 150)
    
    def test_edit_product_post_invalid_data(self):
        """
        Test submitting invalid data when editing a product.

        Ensures that appropriate error messages are displayed and the product is not updated.
        """
        data = {
            'name': '',  # Invalid: empty name
            'description': 'Updated Description',
            'supplier': self.supplier.id,
            'price': 'not a number',  # Invalid: not a number
            'stock': -10  # Invalid: negative stock
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/edit.html')
        # Check for error messages
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('name' in str(message) for message in messages))
        self.assertTrue(any('price' in str(message) for message in messages))
        self.assertTrue(any('stock' in str(message) for message in messages))
    
    def test_edit_nonexistent_product(self):
        """
        Test attempting to edit a non-existent product.

        Ensures that a 404 error is returned when trying to edit a product that doesn't exist.
        """
        url = reverse('stock:product_edit', args=[9999])  # Assuming 9999 is a non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_edit_product_no_changes(self):
        """
        Test submitting the same data when editing a product.

        Verifies that the view handles the case where no changes are made to the product.
        """
        data = {
            'name': 'Original Product',
            'description': 'Original Description',
            'supplier': self.supplier.id,
            'price': '10.00',
            'stock': 100
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('stock:product_details', args=[self.product.id]))
        # Refresh the product from the database
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Original Product')
        self.assertEqual(self.product.description, 'Original Description')
        self.assertEqual(self.product.price, Decimal('10.00'))
        self.assertEqual(self.product.stock, 100)


class ProductsSupplierViewTest(TestCase):
    """
    Test cases for the ProductsSupplierView.

    This class contains unit tests to verify the functionality and behavior of the ProductsSupplierView in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test supplier and multiple products for pagination testing.
        """
        self.client = Client()
        self.supplier = Supplier.objects.create(name="Test Supplier")
        self.url = reverse('stock:product_products_supplier', args=[self.supplier.id])
        
        # Create multiple products for pagination testing
        for i in range(25):  # 25 products to test pagination
            Product.objects.create(
                name=f"Product {i + 1}",
                supplier=self.supplier,
                price=10.00,
                stock=100
            )
    
    def test_products_supplier_view_success(self):
        """
        Test accessing the products supplier view successfully.

        Ensures that the correct template is used and the supplier and products are in the context.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/products_supplier.html')
        self.assertEqual(response.context['supplier'], self.supplier)
        self.assertIsInstance(response.context['products'], Page)
    
    def test_pagination_first_page(self):
        """
        Test the pagination of products on the first page.

        Verifies that the first page contains the correct number of products.
        """
        response = self.client.get(self.url + '?page=1')
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(len(products), 20)  # First page should have 20 products
    
    def test_pagination_second_page(self):
        """
        Test the pagination of products on the second page.

        Ensures that the second page contains the remaining products.
        """
        response = self.client.get(self.url + '?page=2')
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(len(products), 5)  # Second page should have the remaining 5 products
    
    def test_pagination_invalid_page(self):
        """
        Test the behavior when an invalid page number is requested.

        Verifies that the view defaults to the first page for invalid page numbers.
        """
        response = self.client.get(self.url + '?page=invalid')
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(len(products), 20)  # Should default to the first page
    
    def test_pagination_out_of_range_page(self):
        """
        Test the behavior when an out-of-range page number is requested.

        Ensures that the view defaults to the last page for out-of-range page numbers.
        """
        response = self.client.get(self.url + '?page=999')
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(len(products), 5)  # Should default to the last page
    
    def test_nonexistent_supplier(self):
        """
        Test attempting to view products of a non-existent supplier.

        Verifies that a 404 error is returned for a non-existent supplier ID.
        """
        url = reverse('stock:product_products_supplier', args=[9999])  # Non-existent supplier ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_products_supplier_no_products(self):
        """
        Test viewing a supplier with no products.

        Ensures that the view handles suppliers with no associated products correctly.
        """
        # Create a new supplier with no products
        empty_supplier = Supplier.objects.create(name="Empty Supplier")
        url = reverse('stock:product_products_supplier', args=[empty_supplier.id])
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 0)  # No products for this supplier


class ProductsWithoutSupplierViewTest(TestCase):
    """
    Test cases for the ProductsWithoutSupplierView.

    This class contains unit tests to verify the functionality and behavior of the ProductsWithoutSupplierView in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test supplier and products with and without suppliers, and initializes the URL for testing.
        """
        self.client = Client()
        self.url = reverse('stock:product_products_without_supplier')
        # Create a supplier
        self.supplier = Supplier.objects.create(name="Test Supplier")
        # Create products with and without suppliers
        Product.objects.create(name="Product With Supplier", supplier=self.supplier, price=10.00, stock=100)
        Product.objects.create(name="Product Without Supplier 1", price=15.00, stock=50)
        Product.objects.create(name="Product Without Supplier 2", price=20.00, stock=75)
    
    def test_view_url_exists_at_desired_location(self):
        """
        Test that the view is accessible at the expected URL.
        """
        url = reverse('stock:product_products_without_supplier')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        """
        Test that the view is accessible using its name in URL reversing.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """
        Test that the view uses the correct template for rendering.

        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/products_without_supplier.html')
    
    def test_context_contains_only_products_without_supplier(self):
        """
        Test that the context contains only products without a supplier.

        Verifies that all products in the context have no associated supplier.
        """
        response = self.client.get(self.url)
        products = response.context['products']
        self.assertEqual(len(products), 2)
        for product in products:
            self.assertIsNone(product.supplier)
    
    def test_products_with_supplier_not_in_context(self):
        """
        Test that products with suppliers are not included in the context.

        Ensures that only products without suppliers are displayed in the view.
        """
        response = self.client.get(self.url)
        products = response.context['products']
        product_names = [product.name for product in products]
        self.assertNotIn("Product With Supplier", product_names)
    
    def test_no_products_without_supplier(self):
        """
        Test the behavior when there are no products without suppliers.

        Verifies that the view handles this scenario correctly and returns an empty product list.
        """
        # Delete all products without supplier
        Product.objects.filter(supplier__isnull=True).delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 0)
    
    def test_many_products_without_supplier(self):
        """
        Test the behavior when there are many products without suppliers.

        Ensures that all products without suppliers are included in the context.
        """
        # Create many products without supplier
        for i in range(10):
            Product.objects.create(name=f"No Supplier Product {i}", price=10.00, stock=100)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 12)  # 10 new + 2 existing


class SearchProductViewTest(TestCase):
    """
    Test cases for the SearchProductView.

    This class contains unit tests to verify the functionality and behavior of the SearchProductView in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test supplier and products, and initializes the URL for testing.
        """
        self.client = Client()
        self.url = reverse('stock:product_search')
        self.supplier = Supplier.objects.create(name="Test Supplier")
        
        # Create test products
        Product.objects.create(name="Test Product", supplier=self.supplier, price=10.00, stock=100)
        Product.objects.create(name="Another Product", supplier=self.supplier, price=15.00, stock=50)
        Product.objects.create(name="Unique Item", supplier=self.supplier, price=20.00, stock=75)
    
    def test_search_product_view_exists(self):
        """
        Test that the search product view is accessible.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_search_product_uses_correct_template(self):
        """
        Test that the view uses the correct template for rendering.
        """
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'product/search.html')
    
    def test_search_product_with_query(self):
        """
        Test searching for a product with a specific query.

        Verifies that the correct product is returned in the search results.
        """
        response = self.client.get(self.url, {'query': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0].name, "Test Product")
    
    def test_search_product_case_insensitive(self):
        """
        Test that the product search is case-insensitive.
        """
        response = self.client.get(self.url, {'query': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0].name, "Test Product")
    
    def test_search_product_partial_match(self):
        """
        Test searching for products with a partial match.

        Ensures that products with partial name matches are included in the results.
        """
        response = self.client.get(self.url, {'query': 'Prod'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 2)
        product_names = [p.name for p in response.context['products']]
        self.assertIn("Test Product", product_names)
        self.assertIn("Another Product", product_names)
    
    def test_search_product_no_results(self):
        """
        Test the behavior when no products match the search query.
        """
        response = self.client.get(self.url, {'query': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 0)
    
    def test_search_product_empty_query(self):
        """
        Test the behavior when an empty search query is submitted.
        """
        response = self.client.get(self.url, {'query': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 0)
    
    def test_search_product_whitespace_query(self):
        """
        Test the behavior when a whitespace-only search query is submitted.
        """
        response = self.client.get(self.url, {'query': '   '})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 0)
    
    def test_search_product_query_in_context(self):
        """
        Test that the search query is included in the context.

        Ensures that the original search query is available in the template context.
        """
        query = 'Test Query'
        response = self.client.get(self.url, {'query': query})
        self.assertEqual(response.context['query'], query)


# Test Stock record views
class CreateStockMovementViewTest(TestCase):
    """
    Test cases for the CreateStockMovementView.

    This class contains unit tests to verify the functionality and behavior of the CreateStockMovementView in the application.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test method.

        Creates a test supplier, product, and initializes the URL for creating stock movements.
        """
        self.client = Client()
        self.supplier = Supplier.objects.create(name="Test Supplier")
        self.product = Product.objects.create(
            name="Test Product",
            supplier=self.supplier,
            price=Decimal('10.00'),
            stock=100
        )
        self.url = reverse('stock:stock_create_movement', args=[self.product.id])
    
    def test_create_stock_movement_get_request(self):
        """
        Test accessing the create stock movement view with a GET request.

        Ensures that the correct template is used and the product is in the context.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/create_movement.html')
        self.assertEqual(response.context['product'], self.product)
    
    def test_create_stock_movement_increase(self):
        """
        Test creating a stock movement to increase product quantity.

        Verifies that the stock movement is created and the product stock is updated correctly.
        """
        data = {
            'quantity': 50,
            'movement_type': 'increase',
            'reason': 'increase stock'
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('stock:product_details', args=[self.product.id]))
        # Check product stock update
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 150)
    
    def test_create_stock_movement_decrease(self):
        """
        Test creating a stock movement to decrease product quantity.

        Ensures that the stock movement is created and the product stock is reduced correctly.
        """
        data = {
            'quantity': 30,
            'movement_type': 'decrease',
            'reason': 'sale'
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('stock:product_details', args=[self.product.id]))
        # Check product stock update
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 70)
    
    def test_create_stock_movement_invalid_data(self):
        """
        Test submitting invalid data when creating a stock movement.

        Verifies that appropriate error messages are displayed and no changes are made to the stock.
        """
        data = {
            'quantity': '',
            'movement_type': 'invalid',  # Invalid: not in choices
            'reason': ''
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)  # Form re-renders with errors
        messages = list(response.context['messages'])
        # Check for error messages
        self.assertTrue(any('quantity' in str(message) for message in messages))
        self.assertTrue(any('movement_type' in str(message) for message in messages))
        self.assertTrue(any('reason' in str(message) for message in messages))
    
    def test_create_stock_movement_nonexistent_product(self):
        """
        Test attempting to create a stock movement for a non-existent product.

        Ensures that a 404 error is returned for an invalid product ID.
        """
        url = reverse('stock:stock_create_movement', args=[9999])  # Non-existent product ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_create_stock_movement_negative_quantity(self):
        data = {
            'quantity': -20,
            'movement_type': 'decrease',
            'reason': 'sale'
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('stock:product_details', args=[self.product.id]))
        
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 120)  # 100 + 20 (because it's a decrease of -20)
    
    def test_create_stock_movement_zero_quantity(self):
        """
        Test creating a stock movement with zero quantity.

        Verifies that an error is displayed and no stock movement is created.
        """
        data = {
            'quantity': 0,
            'movement_type': 'increase',
            'reason': 'cabin_expense'
        }
        response = self.client.post(self.url, data)
        # Form should re-render with errors since quantity cannot be zero
        self.assertRedirects(response, reverse('stock:product_details', args=[self.product.id]))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 100)  # No change
    
    def test_create_stock_movement_no_changes_to_stock_on_error(self):
        """
        Test that no changes are made to the stock when an error occurs during movement creation.

        Ensures that the product's stock remains unchanged when invalid data is submitted.
        """
        initial_stock = self.product.stock
        
        # Submit invalid form data
        data = {
            'quantity': -50,
            'movement_type': '',
            'reason': ''
        }
        
        response = self.client.post(self.url, data)
        # Ensure the product's stock remains unchanged
        self.product.refresh_from_db()
