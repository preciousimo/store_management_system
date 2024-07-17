from django.contrib import admin
from django.contrib.admin import actions
from .forms import StockCreateForm
from .models import Stock, Category, StockHistory
import csv 
from django.http import HttpResponse

class StockHistoryInline(admin.TabularInline):
    model = StockHistory
    extra = 1 

class StockCreateAdmin(admin.ModelAdmin):
    list_display = ['category', 'item_name', 'quantity']
    form = StockCreateForm
    list_filter = ['category']
    search_fields = ['category', 'item_name']
    inlines = [StockHistoryInline]
    readonly_fields = ('last_updated', 'timestamp')

    @admin.action(description='Export Selected Items to CSV')
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="stock_items.csv"'
        writer = csv.writer(response)

        writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])

        for stock in queryset:
            writer.writerow([stock.category, stock.item_name, stock.quantity])

        return response

    actions = [export_to_csv]

admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Category)
admin.site.register(StockHistory)