from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
# Create your models here.
class ItemCategory(models.Model):
    name = models.CharField(max_length=127, verbose_name="Category Name")
    payload_code = models.CharField(max_length=127, editable=False)


    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(ItemCategory, verbose_name="Item Category")
    name = models.CharField(max_length=127, verbose_name="Item Name")
    price = models.DecimalField(verbose_name="Unit Price", decimal_places=3, max_digits=8)
    image = models.CharField(max_length=127, verbose_name="Item Image")
    postback_code = models.CharField(max_length=127, editable=False)

    def save(self, *args, **kwargs):
        self.postback_code = 'item.'+str(self.pk)
        super(Item, self).save(*args, **kwargs)



    def __str__(self):
        return self.name


class PendingOrder(models.Model):
    customer_id = models.CharField(max_length=127)
    customer_name = models.CharField(max_length=127)
    address = models.TextField(default='NS')
    phone = models.CharField(max_length=127, default='NS')
    email = models.EmailField(default='NS')
    bkash_transaction_no = models.CharField(max_length=127, default='NS')
    is_confirmed = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    order_date = models.DateField(auto_now_add=True)
    order_time = models.TimeField(auto_now_add=True)
    recipt_provided = models.BooleanField(default=False)
    cart = JSONField(null=True, blank=True)

    def __str__(self):
        return self.customer_name + str(self.pk)



@receiver(post_save, sender=ItemCategory)
def assign_payload(sender, instance, created,**kwargs):
    if created:
        instance.payload_code = "cat."+str(instance.pk)
        instance.save()

@receiver(post_save, sender=Item)
def assign_postback(sender, instance, created,**kwargs):
    if created:
        instance.postback_code = "itm."+str(instance.pk)
        instance.save()