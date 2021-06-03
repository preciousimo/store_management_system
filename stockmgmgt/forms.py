from django import forms
from .models import Stock


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']

        # To prevent saving object with a blank item name
        def clean_category(self):
            category = self.cleaned_data.get('category')
            if not category:
                raise forms.ValidationError('This field is required')
            for instance in Stock.objects.all():

                # Alerting and preventing the duplicate entry of computer name
                if instance.category == category:
                    raise forms.ValidationError(
                        str(category) + ' is already created')

            return category

        def clean_item_name(self):
            item_name = self.cleaned_data.get('item_name')
            if not item_name:
                raise forms.ValidationError('This field is required')
            return item_name


class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)

    class Meta:
        model = Stock
        fields = ['category', 'item_name']


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']


class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issue_quantity', 'issue_to']


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity']
