from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class Stock(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    supplier = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default=0, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return self.item_name + ' ' + str(self.quantity)

# Create a StockHistory model with the relevant fields
class StockHistory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=50, choices=[('issue', 'Issue'), ('receive', 'Receive')], default='issue')
    quantity = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=50, blank=True, null=True) 
    supplier = models.CharField(max_length=50, blank=True, null=True) 
    issue_to = models.CharField(max_length=50, blank=True, null=True) 

    def __str__(self):
        return f"{self.action} of {self.quantity} {self.stock.item_name}"

@receiver(post_save, sender=Stock)
def stock_history_update(sender, instance, created, **kwargs):
    if not created:  # Only log changes, not initial creation
        try:
            StockHistory.objects.create(
                stock=instance,
                action='receive' if instance.receive_quantity else 'issue',  
                quantity=instance.receive_quantity if instance.receive_quantity else instance.issue_quantity,
                user=str(instance.receive_by) if instance.receive_quantity else str(instance.issue_by),
                supplier=instance.supplier if instance.receive_quantity else None,
                issue_to=instance.issue_to if instance.issue_quantity else None
            )
            instance.receive_quantity = 0
            instance.issue_quantity = 0
            instance.save()
        except Exception as e:
            print(f"Error creating StockHistory: {e}")