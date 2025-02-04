from decimal import Decimal

from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TransactionForm
from .models import Transaction
from client.models import Client, ClientVoucher
from appointment.models import Appointment
from service.models import Service


def client_payment_history(request, client_id):
    """
    Display the payment history for a specific client.

    This view retrieves all transactions for a given client, orders them by date, and paginates the results.

    :param request: The HTTP request object.
    :param client_id: The ID of the client whose payment history is being viewed.
    :return: Rendered HTML page with the client's payment history.

    :raises Http404: If the client with the given ID does not exist.
    """
    client = get_object_or_404(Client, id=client_id)
    transactions = Transaction.objects.filter(client=client).order_by('-date')
    
    # Pagination with 20 payment per page
    paginator = Paginator(transactions, 30)
    page_number = request.GET.get('page')
    try:
        payments = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        payments = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of results
        payments = paginator.page(paginator.num_pages)
        
    return render(
        request,
        'sales/client_payment_history.html',
        {'client': client, 'transactions': transactions, 'payments': payments}
    )


def delete_transaction(request, transaction_id):
    """
    Delete a specific transaction.

    This view handles the deletion of a transaction. It requires a POST request to actually delete the transaction.

    :param request: The HTTP request object.
    :param transaction_id: The ID of the transaction to be deleted.
    :return: Redirect to the payment list page after successful deletion, or confirmation page for GET requests.
    :raises Http404: If the transaction with the given ID does not exist.
    """
    transaction = get_object_or_404(Transaction, id=transaction_id)
    
    if request.method == 'POST':
        transaction.delete()
        
        messages.success(
            request,
            f"La transacción ha sido eliminada correctamente."
        )
        return redirect('sales:list_payment')
    
    return render(request, 'sales/delete.html', {'transaction': transaction})


def list_payment(request):
    """
    Display a list of all transactions.

    This view retrieves all transactions, orders them by date, and paginates the results.
    It also prefetches related data to optimize database queries.

    :param request: The HTTP request object.
    :return: Rendered HTML page with the list of transactions.
    """
    # Transaction with related sales, services and details
    transactions = Transaction.objects.select_related('client', 'appointment').prefetch_related(
        'appointment__services').order_by('-date')
   
    # Pagination with 20 sales per page
    paginator = Paginator(transactions, 30)
    page_number = request.GET.get('page')
    try:
        list_transactions = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        list_transactions = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of results
        list_transactions = paginator.page(paginator.num_pages)
    
    # Get the first client if there are transactions
    client = transactions[0].client if transactions else None
    
    context = {'list_transactions': list_transactions, 'transactions': transactions}
    if client:
        context['client'] = client
        
    return render(request, 'sales/list_payment.html', context)


def register_transaction(request, appointment_id=None):
    """
    Register a new transaction or edit an existing one.

    This view handles both GET and POST requests for registering a new transaction or editing an existing one. It
    processes transaction and payment forms.

    :param request: The HTTP request object.
    :param appointment_id: The ID of the appointment associated with the transaction (optional).
    :return: Rendered HTML page with transaction forms or redirect to payment list.

    :raises Http404: If the appointment with the given ID does not exist.
    """
    # Get appointment and client
    appointment = get_object_or_404(Appointment, id=appointment_id)
    client = appointment.client
    total_amount = sum(service.price for service in appointment.services.all())  # Initialize total_amount
    
    if request.method == 'POST':
        # Pre-calculate total_amount
        selected_services = request.POST.getlist('services')
        services = Service.objects.filter(id__in=selected_services)
        total_amount = services.aggregate(total=Sum('price'))['total'] or Decimal('0')
        
        transaction_form = TransactionForm(request.POST)

        if transaction_form.is_valid():
            
            # Create transaction object
            transaction = transaction_form.save(commit=False)
            transaction.client = client
            transaction.appointment = appointment
            transaction.total_amount = total_amount
            transaction.save()
            transaction.services.set(transaction_form.cleaned_data['services'])  # Assign the services
            
            messages.success(request, "Transacción registrada exitosamente.")
            return redirect("sales:list_payment")
        else:
            for form in [transaction_form]:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Error en {field}: {error}")
   
    else:
        transaction_form = TransactionForm(initial={
            'client': client.id,
            'total_amount': total_amount,
            'services': appointment.services.all()
        })
    
    return render(request, 'sales/register_transaction.html', {
        'transaction_form': transaction_form,
        'appointment': appointment,
        'services': appointment.services.all(),
        'total_amount': total_amount,
    })




