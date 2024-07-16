from django.db import models
from django.urls import reverse

# Create your models here.
category_choice = (
    ('Furniture', 'Furniture'),
    ('IT Equipment', 'IT Equipment'),
    ('Phone', 'Phone'),
)

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Enforce uniqueness

    def __str__(self):
        return self.name

class StockItem(models.Model):  # Renamed to StockItem
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50, unique=True) # Enforce uniqueness
    quantity = models.IntegerField(default=0)  # Remove unnecessary default
    reorder_level = models.IntegerField(default=0)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name + ' ' + str(self.quantity)

    def get_absolute_url(self):
        return reverse('stock_detail', kwargs={'pk': self.pk})  # Add a get_absolute_url method


class StockAction(models.Model):
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=10, choices=[
        ('receive', 'Receive'),
        ('issue', 'Issue')
    ])
    quantity = models.IntegerField()
    supplier = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    performed_by = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.action_type == 'receive':
            self.item.quantity += self.quantity
        elif self.action_type == 'issue':
            self.item.quantity -= self.quantity
        self.item.save()