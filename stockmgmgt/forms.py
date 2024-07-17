from django import forms
from django.core.exceptions import ValidationError
from .models import Stock, StockHistory, Category

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']
        labels = {
            'category': 'Item Category',
            'item_name': 'Item Name',
            'quantity': 'Available Quantity',
        }

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required')
        return category

class StockHistorySearchForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category')
    item_name = forms.CharField(required=False, label='Item Name')
    start_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label='Start Date')
    end_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label='End Date')
    export_to_CSV = forms.BooleanField(required=False, label='Export to CSV')

    class Meta:
        model = StockHistory
        fields = ['stock__category', 'stock__item_name', 'start_date', 'end_date']  # Use stock__ to access related fields

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required')
        return category

class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)

    class Meta:
        model = Stock
        fields = ['category', 'item_name']

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required')
        return category

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required')
        return category

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        return item_name

class StockIssueForm(forms.Form):
    issue_quantity = forms.IntegerField(label="Issue Quantity", min_value=1)
    issue_to = forms.CharField(label="Issue To", max_length=50) 
    
    def clean_issue_quantity(self):
        issue_quantity = self.cleaned_data.get('issue_quantity')
        stock_pk = self.initial['stock_pk']  # Get stock ID from initial data
        stock = Stock.objects.get(pk=stock_pk)  # Get the stock object 
        quantity = stock.quantity
        if issue_quantity > quantity:
            raise ValidationError("Issue quantity cannot exceed available quantity.")
        return issue_quantity 

class StockReceiveForm(forms.Form):
    receive_quantity = forms.IntegerField(label="Receive Quantity", min_value=1)
    supplier = forms.CharField(label="Supplier", max_length=50)

class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']

        widgets = {
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
        }