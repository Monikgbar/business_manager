from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ProductForm, StockMovementForm
from .models import Product, Supplier


# Supplier views
def add_supplier(request):
    """
    Add a new supplier.

    This view handles POST requests for adding a new supplier.
    It creates a new Supplier object with the provided name.

    :param request: The HTTP request object.
    :return: Redirect to the supplier list page.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            if not Supplier.objects.filter(name=name).exists():
                Supplier.objects.create(name=name)
                messages.success(request, f"Proveedor '{name}' añadido correctamente.")
            else:
                messages.error(request, f"El proveedor '{name}' ya existe.")
        else:
            messages.error(request, "El nombre del proveedor no puede estar vacío.")
    return redirect('stock:supplier_list')


def edit_supplier(request, supplier_id):
    """
    Edit an existing supplier.

    This view handles POST requests for editing a supplier.
    It updates the name of the supplier with the given ID.

    :param request: The HTTP request object.
    :param supplier_id: The ID of the supplier to be edited.
    :return: Redirect to the products page for the supplier.
    :raises Http404: If the supplier with the given ID does not exist.
    """
    supplier = get_object_or_404(Supplier, id=supplier_id)
    
    if request.method == 'POST':
        supplier.name = request.POST.get('name')
        supplier.save()
    return redirect(reverse('stock:product_products_supplier', args=[supplier_id]))
    

def delete_supplier(request, supplier_id):
    """
    Delete a specific supplier.

    This view handles POST requests for deleting a supplier.
    It deletes the supplier with the given ID.

    :param request: The HTTP request object.
    :param supplier_id: The ID of the supplier to be deleted.
    :return: Redirect to the supplier list page.
    :raises Http404: If the supplier with the given ID does not exist.
    """
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        supplier.delete()
    return redirect('stock:supplier_list')


def list_supplier(request):
    """
    Display a list of all suppliers and products without a supplier.

    This view retrieves all suppliers and products that do not belong to any supplier.

    :param request: The HTTP request object.
    :return: Rendered HTML page with the list of suppliers and products without a supplier.
    """
    suppliers = Supplier.objects.all().order_by('name')
    product_without_supplier = Product.objects.filter(supplier__isnull=True)
    
    return render(
        request,
        'supplier/list.html',
        {'suppliers': suppliers, 'product_without_supplier': product_without_supplier}
    )


# Product views
def add_products(request):
    """
    Add a new product.

    This view handles both GET and POST requests for adding a new product.
    It renders a form for product creation and processes the form submission.

    :param request: The HTTP request object.
    :return: Rendered HTML page with the product creation form or redirect to supplier list.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('stock:supplier_list'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProductForm()
    
    return render(request, 'product/add.html', {'form': form})


def delete_product(request, product_id):
    """
    Delete a specific product.

    This view handles the deletion of a product. It requires a POST request to actually delete the product.

    :param request: The HTTP request object.
    :param product_id: The ID of the product to be deleted.
    :return: Redirect to the supplier list page after successful deletion, or confirmation page for GET requests.
    :raises Http404: If the product with the given ID does not exist.
    """
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.delete()
        
        return redirect('stock:supplier_list')
    
    return render(request, 'product/delete.html', {'product': product})


def details_product(request, product_id):
    """
    Display details of a specific product.

    This view retrieves and displays the details of a single product.

    :param request: The HTTP request object.
    :param product_id: The ID of the product to be viewed.
    :return: Rendered HTML page with the product details.
    :raises Http404: If the product with the given ID does not exist.
    """
    product = get_object_or_404(Product, id=product_id)
    
    return render(request, 'product/details.html', {'product': product})


def edit_product(request, product_id):
    """
    Edit an existing product.

    This view handles both GET and POST requests for editing a product.
    It retrieves the product details, renders a form for editing, and processes the form submission.

    :param request: The HTTP request object.
    :param product_id: The ID of the product to be edited.
    :return: Rendered HTML page with the product edit form or redirect to product details.
    :raises Http404: If the product with the given ID does not exist.
    """
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse('stock:product_details', args=[product.id]))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProductForm(instance=product)
  
    return render(request, 'product/edit.html', {'form': form, 'product': product})


def products_supplier(request, supplier_id):
    """
    Display products for a specific supplier.

    This view retrieves all products for a given supplier and paginates the results.

    :param request: The HTTP request object.
    :param supplier_id: The ID of the supplier whose products are being viewed.
    :return: Rendered HTML page with the list of products for the supplier.
    :raises Http404: If the supplier with the given ID does not exist.
    """
    supplier = get_object_or_404(Supplier, id=supplier_id)
    products = supplier.products.all()
    
    # Pagination with 20 services per page
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range get last page of results
        products = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        products = paginator.page(1)
    
    return render(
        request, 'product/products_supplier.html', {'supplier': supplier, 'products': products}
    )


def products_without_supplier(request):
    """
    Display products that do not belong to any supplier.

    This view retrieves all products that have no associated supplier.

    :param request: The HTTP request object.
    :return: Rendered HTML page with the list of products without a supplier.
    """
    products = Product.objects.filter(supplier__isnull=True)
    
    return render(request, 'product/products_without_supplier.html', {'products': products})


def search_product(request):
    """
    Search for products based on a query.

    This view handles searching for products based on the provided query.

    :param request: The HTTP request object.
    :return: Rendered HTML page with the search results.
    """
    query = request.GET.get('query', '').strip()
    
    products = Product.objects.filter(name__icontains=query) if query else []

    return render(request, 'product/search.html', {'query': query, 'products': products})
    

# Stock record views
def create_stock_movement(request, product_id):
    """
    Create a new stock movement for a specific product.

    This view handles both GET and POST requests for creating a new stock movement.
    It renders a form for stock movement creation and processes the form submission.
    After successful creation, it updates the product's stock accordingly.

    :param request: The HTTP request object.
    :param product_id: The ID of the product for which the stock movement is being created.
    :return: Rendered HTML page with the stock movement creation form or redirect to product details.
    :raises Http404: If the product with the given ID does not exist.
    """
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            stock_movement = form.save(commit=False)
            stock_movement.product = product
            stock_movement.save()
            
            # Update product stock
            if stock_movement.movement_type == 'increase':
                product.stock += stock_movement.quantity
            elif stock_movement.movement_type == 'decrease':
                product.stock -= stock_movement.quantity
            product.save()
            
            return redirect(reverse('stock:product_details', args=[product_id]))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = StockMovementForm(initial={'product': product})

    return render(request, 'stock/create_movement.html', {'form': form, 'product': product})