from itertools import groupby

from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CategoryForm, ServiceForm, VoucherForm
from .models import Category, Service, Voucher


# Service views
def add_service(request):
    """
    Add a new service.

    This view handles both GET and POST requests for adding a new service.
    It renders a form for service creation and processes the form submission.

    :param request: The HTTP request object.
    :return: Rendered HTML page with the service creation form or redirect to category list.
    """
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('service:category_list'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ServiceForm()
        print(form.errors)
    return render(request, 'service/add.html', {'form': form})


def edit_service(request, service_id):
    """
    Edit an existing service.

    This view handles both GET and POST requests for editing a service.
    It retrieves the service details, renders a form for editing, and processes the form submission.

    :param request: The HTTP request object.
    :param service_id: The ID of the service to be edited.
    :return: Rendered HTML page with the service edit form or redirect to service view.
    :raises Http404: If the service with the given ID does not exist.
    """
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect(reverse('service:service_view', args=[service.id]))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ServiceForm(instance=service)
  
    return render(
        request,
        'service/edit.html',
        {'form': form, 'service': service}
    )


def delete_service(request, service_id):
    """
    Delete a specific service.

    This view handles the deletion of a service. It requires a POST request to actually delete the service.

    :param request: The HTTP request object.
    :param service_id: The ID of the service to be deleted.
    :return: Redirect to the category list page after successful deletion, or confirmation page for GET requests.
    :raises Http404: If the service with the given ID does not exist.
    """
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        service.delete()
        
        return redirect('service:category_list')
    
    return render(request, 'service/delete.html', {'service': service})


def services_category(request, category_id):
    """
    Display services for a specific category.

    This view retrieves all services for a given category and paginates the results.

    :param request: The HTTP request object.
    :param category_id: The ID of the category whose services are being viewed.
    :return: Rendered HTML page with the list of services for the category.
    :raises Http404: If the category with the given ID does not exist.
    """
    category = get_object_or_404(Category, id=category_id)
    services = category.services.all()
    
    # Pagination with 20 services per page
    paginator = Paginator(services, 20)
    page_number = request.GET.get('page')
    try:
        services = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range get last page of results
        services = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        services = paginator.page(1)
    
    return render(
        request, 'service/services_category.html', {'category': category, 'services': services}
    )


def services_without_category(request):
    """
    Display services that do not belong to any category.

    This view retrieves all services that have no associated category.

    :param request: The HTTP request object.
    :return: Rendered HTML page with the list of services without a category.
    """
    services = Service.objects.filter(category__isnull=True)
    
    return render(request, 'service/services_without_category.html', {'services': services})


def view_details_service(request, service_id):
    """
    Display details of a specific service.

    This view retrieves and displays the details of a single service.

    :param request: The HTTP request object.
    :param service_id: The ID of the service to be viewed.
    :return: Rendered HTML page with the service details.
    :raises Http404: If the service with the given ID does not exist.
    """
    service = get_object_or_404(Service, id=service_id)
    
    return render(request, 'service/view.html', {'service': service})


# Category views
def add_category(request):
    """
    Add a new category.

    This view handles both GET and POST requests for adding a new category.
    It renders a form for category creation and processes the form submission.

    :param request: The HTTP request object.
    :return: Rendered HTML page with the category creation form or redirect to category list.
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('service:category_list'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CategoryForm()
    
    return render(request, 'category/add.html', {'form': form})


def edit_category(request, category_id):
    """
    Edit an existing category.

    This view handles both GET and POST requests for editing a category.
    It retrieves the category details, renders a form for editing, and processes the form submission.

    :param request: The HTTP request object.
    :param category_id: The ID of the category to be edited.
    :return: Rendered HTML page with the category edit form or redirect to category list.
    :raises Http404: If the category with the given ID does not exist.
    """
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect(reverse('service:category_list'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CategoryForm(instance=category)
    
    return render(
        request,
        'category/edit.html',
        {'form': form, 'category': category}
    )


def delete_category(request, category_id):
    """
    Delete a specific category.

    This view handles the deletion of a category. It requires a POST request to actually delete the category.

    :param request: The HTTP request object.
    :param category_id: The ID of the category to be deleted.
    :return: Redirect to the category list page after successful deletion, or confirmation page for GET requests.
    :raises Http404: If the category with the given ID does not exist.
    """
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category.delete()
        
        return redirect('service:category_list')
    
    return render(request, 'category/delete.html', {'category': category})


def list_category(request):
    """
    Display a list of all categories and services without a category.

    This view retrieves all categories and services that do not belong to any category.

    :param request: The HTTP request object.
    :return: Rendered HTML page with the list of categories and services without a category.
    """
    categories = Category.objects.all().order_by('name')
    services_without_category = Service.objects.filter(category__isnull=True)
    
    return render(
        request,
        'category/list.html',
        {'categories': categories, 'services_without_category': services_without_category}
    )


# Voucher views
def add_voucher(request):
    """
    Add a new voucher.

    This view handles both GET and POST requests for adding a new voucher.
    It renders a form for voucher creation and processes the form submission.

    :param request: The HTTP request object.
    :return: Rendered HTML page with the voucher creation form or redirect to voucher list.
    """
    services = Service.objects.select_related('category').all().order_by('category__name', 'name')
    services_by_category = []
    for category, items in groupby(services, lambda s: s.category):
        services_by_category.append({
            'category': category,
            'services': list(items)
        })

    if request.method == 'POST':
        
        form = VoucherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('service:voucher_list'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = VoucherForm()
    
    return render(
        request,
        'voucher/add.html',
        {'form': form, 'services_by_category': services_by_category}
    )


def delete_voucher(request, voucher_id):
    """
    Delete a specific voucher.

    This view handles the deletion of a voucher. It requires a POST request to actually delete the voucher.

    :param request: The HTTP request object.
    :param voucher_id: The ID of the voucher to be deleted.
    :return: Redirect to the voucher list page after successful deletion, or confirmation page for GET requests.
    :raises Http404: If the voucher with the given ID does not exist.
    """
    voucher = get_object_or_404(Voucher, id=voucher_id)
    
    if request.method == 'POST':
        voucher.delete()
        
        return redirect('service:voucher_list')
    
    return render(request, 'voucher/delete.html', {'voucher': voucher})


def details_voucher(request, voucher_id):
    """
    Display details of a specific voucher.

    This view retrieves and displays the details of a single voucher.

    :param request: The HTTP request object.
    :param voucher_id: The ID of the voucher to be viewed.
    :return: Rendered HTML page with the voucher details.
    :raises Http404: If the voucher with the given ID does not exist.
    """
    voucher = get_object_or_404(Voucher, id=voucher_id)
    
    return render(request, 'voucher/details.html', {'voucher': voucher})


def edit_voucher(request, voucher_id):
    """
    Edit an existing voucher.

    This view handles both GET and POST requests for editing a voucher.
    It retrieves the voucher details, renders a form for editing, and processes the form submission.

    :param request: The HTTP request object.
    :param voucher_id: The ID of the voucher to be edited.
    :return: Rendered HTML page with the voucher edit form or redirect to voucher details.
    :raises Http404: If the voucher with the given ID does not exist.
    """
    voucher = get_object_or_404(Voucher, id=voucher_id)
    services = Service.objects.select_related('category').all().order_by('category__name', 'name')
    services_by_category = [
        {'category': category, 'services': list(items)}
        for category, items in groupby(services, lambda s: s.category)
    ]
    
    if request.method == 'POST':
        form = VoucherForm(request.POST, instance=voucher)
        if form.is_valid():
            form.save()
            return redirect(reverse('service:voucher_details', args=[voucher.id]))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = VoucherForm(instance=voucher)
        form.fields['services'].initial = voucher.services.all()

    return render(
        request,
        'voucher/edit.html',
        {'form': form, 'voucher': voucher, 'services_by_category': services_by_category})


def voucher_list(request):
    """
    Display a list of all vouchers.

    This view retrieves all vouchers and paginates the results.

    :param request: The HTTP request object.
    :return: Rendered HTML page with the list of vouchers.
    """
    vouchers = Voucher.objects.all().order_by('name')
    
    # Pagination with 20 vouchers per page
    paginator = Paginator(vouchers, 20)
    page_number = request.GET.get('page')
    try:
        vouchers = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range get last page of results
        vouchers = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        vouchers = paginator.page(1)
        
    return render(request, 'voucher/list.html', {'vouchers': vouchers})


# Shared views
def search_items(request, model_name):
    """
    Search for services or vouchers based on a query.

    This view handles searching for services or vouchers based on the provided query and model name.

    :param request: The HTTP request object.
    :param model_name: The name of the model to search ('service' or 'voucher').
    :return: Rendered HTML page with the search results.
    """
    query = request.GET.get('query', '').strip()
    items = []
    
    if model_name == 'service':
        items = Service.objects.filter(name__icontains=query) if query else []
    elif model_name == 'voucher':
        items = Voucher.objects.filter(name__icontains=query) if query else []

    return render(
        request,
        f'shared/search_items.html',
        {'items': items, 'query': query})



