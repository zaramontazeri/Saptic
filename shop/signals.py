from decimal import Decimal
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from shop.models import ProductVariation


@receiver(pre_save,sender=ProductVariation)
def my_callback(sender, instance, *args, **kwargs):
    discount = int(instance.price)
    if instance.occasional_discount:
        percentage = instance.occasional_discount.percentage
        discount = int(float(instance.price) - round((float(percentage) / 100.0) * float(instance.price)))
        instance.discount_price = Decimal(discount)
