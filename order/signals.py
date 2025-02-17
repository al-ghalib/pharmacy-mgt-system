# import logging
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.db import transaction
# from .models import OrderDetail

# logger = logging.getLogger(__name__)


# @receiver(post_save, sender=OrderDetail)
# def reduce_stock(sender, instance, created, **kwargs):
#     if created:
#         try:
#             with transaction.atomic():
#                 inventory = instance.cart_item.inventory
#                 if inventory.stock >= instance.quantity:
#                     inventory.stock -= instance.quantity
#                     inventory.save()
#                 else:
#                     logger.warning(f"Not enough stock for {inventory.medicine.name}")
#         except Exception as e:
#             logger.error(f"Error while reducing stock: {e}")

