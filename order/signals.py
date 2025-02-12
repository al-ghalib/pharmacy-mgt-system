import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import Order, OrderDetail, Cart

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def clear_cart(sender, instance, created, **kwargs):
    if created and instance.status == "confirmed":
        try:
            with transaction.atomic():
                cart = Cart.objects.get(user=instance.user, is_active=True)
                cart.is_active = False
                cart.save()
        except Cart.DoesNotExist:
            logger.warning("No active cart found for user.")


@receiver(post_save, sender=OrderDetail)
def reduce_stock(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                inventory = instance.cart_item.inventory
                if inventory.stock >= instance.quantity:
                    inventory.stock -= instance.quantity
                    inventory.save()
                else:
                    logger.warning(f"Not enough stock for {inventory.medicine.name}")
        except Exception as e:
            logger.error(f"Error while reducing stock: {e}")


@receiver(post_save, sender=OrderDetail)
@receiver(post_delete, sender=OrderDetail)
def update_order_total_price(sender, instance, **kwargs):
    try:
        instance.order.calculate_total_price()
    except Exception as e:
        logger.error(f"Error while updating order total price: {e}")


# import logging
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.db import transaction
# # from product.models import Inventory
# from .models import Order, OrderDetail, Cart


# # @receiver(post_save, sender=Order)
# # def clear_cart(sender, instance, created, **kwargs):
# #     if created and instance.status == "confirmed":
# #         try:
# #             with transaction.atomic():
# #                 cart = Cart.objects.filter(user=instance.user, is_active=True).first()
# #                 if cart:
# #                     cart.is_active = False
# #                     cart.save()
# #         except Exception as e:
# #             print(f"Error while clearing cart: {e}")
# @receiver(post_save, sender=Order)
# def clear_cart(sender, instance, created, **kwargs):
#     if created and instance.status == "confirmed":
#         try:
#             with transaction.atomic():
#                 cart = Cart.objects.get(user=instance.user, is_active=True)
#                 cart.is_active = False
#                 cart.save()
#         except Cart.DoesNotExist:
#             print("No active cart found for user")


# # @receiver(post_save, sender=OrderDetail)
# # def reduce_stock(sender, instance, created, **kwargs):
# #     if created:
# #         order = instance.order
# #         if order.status == "confirmed":
# #             try:
# #                 with transaction.atomic():
# #                     inventory = instance.cart_item.inventory
# #                     if inventory.stock >= instance.quantity:
# #                         inventory.stock -= instance.quantity
# #                         inventory.save()
# #                     else:
# #                         print(f"Not enough stock for {inventory.medicine.name}")
# #             except Exception as e:
# #                 print(f"Error while reducing stock: {e}")


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
