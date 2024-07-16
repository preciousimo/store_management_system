from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from django.contrib import messages
from .models import Stock, Category, StockHistory
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm, IssueForm, ReceiveForm, ReorderLevelForm, StockHistorySearchForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    title = 'SONIPS STORE MANAGEMENT SYSTEM'
    context = {
        "title": title,
    }
    return redirect('/list_items')  

@login_required
def list_items(request):
    header = 'List of Items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        "form": form,
        "header": header,
        "queryset": queryset,
    }

    if request.method == 'POST':
        if form['item_name'].value():
            queryset = queryset.filter(item_name__icontains=form['item_name'].value())

        if form['export_to_CSV'].value():
            return export_to_csv(queryset) 

    return render(request, "list_items.html", context)

@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/list_items')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_items.html", context)

@login_required
def update_items(request, pk):
    try:
        queryset = Stock.objects.get(id=pk)
    except Stock.DoesNotExist:
        messages.error(request, 'Item not found')
        return redirect('/list_items')

    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Saved')
            return redirect('/list_items')
    context = {
        'form': form
    }
    return render(request, 'add_items.html', context)

@login_required
def delete_items(request, pk):
    try:
        queryset = Stock.objects.get(id=pk)
    except Stock.DoesNotExist:
        messages.error(request, 'Item not found')
        return redirect('/list_items')

    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Deleted Successfully')
        return redirect('/list_items')
    return render(request, 'delete_items.html')

@login_required
def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "queryset": queryset,
    }
    return render(request, "stock_detail.html", context)

@login_required
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) +
                         " " + str(instance.item_name) + "s now left in Store")
        instance.save()

        return redirect('/stock_detail/'+str(instance.id)) 

    context = {
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)

@login_required
def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        instance.receive_by = str(request.user)
        instance.save()
        messages.success(request, "Received SUCCESSFULLY. " +
                         str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

        return redirect('/stock_detail/'+str(instance.id)) 

    context = {
        "title": 'Receive ' + str(queryset.item_name),
        "instance": queryset,
        "form": form,
        "username": 'Receive By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)

@login_required
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.item_name) +
                         " is updated to " + str(instance.reorder_level))

        return redirect("/list_items")
    context = {
        "instance": queryset,
        "form": form,
    }
    return render(request, "add_items.html", context)

@login_required
def list_history(request):
    header = 'LIST OF ITEMS'
    queryset = StockHistory.objects.all()
    form = StockHistorySearchForm(request.POST or None)
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }

    if request.method == 'POST':
        category = form['category'].value()
        start_date = form['start_date'].value()
        end_date = form['end_date'].value()

        if category:
            queryset = queryset.filter(stock__category_id=category)

        if start_date and end_date:  # Only filter if both dates are provided
            queryset = queryset.filter(timestamp__range=[start_date, end_date])

        if form['export_to_CSV'].value():
            return export_to_csv(queryset)

    return render(request, "list_history.html", context)

def export_to_csv(queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
    writer = csv.writer(response)

    writer.writerow(
        ['CATEGORY',
         'ITEM NAME',
         'QUANTITY',
         'ISSUE QUANTITY',
         'RECEIVE QUANTITY',
         'SUPPLIER',
         'RECEIVE BY',
         'ISSUE BY',
         'LAST UPDATED'])
    for stock in queryset:
        writer.writerow(
            [stock.stock.category,
             stock.stock.item_name,
             stock.stock.quantity,
             stock.quantity if stock.action == 'issue' else 0,
             stock.quantity if stock.action == 'receive' else 0,
             stock.supplier,
             stock.user if stock.action == 'receive' else None,
             stock.user if stock.action == 'issue' else None,
             stock.timestamp]
        )
    return response