from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

from django.db import transaction

from product.models import Category, Product

logger = logging.getLogger(__name__)


@shared_task
def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
    )


@shared_task
def process_bulk_upload(data):
    categories = data.get("categories", [])
    products = data.get("products", [])

    if not categories or not products:
        logger.info("No categories or products provided")
        return
    try:
        with transaction.atomic():
            for c in categories:
                obj, created = Category.objects.update_or_create(
                    category_name=c["category_name"],
                    is_deleted=False,
                    defaults={
                        "description": c.get("description", "")
                    }
                )
                logger.info(
                    "%s category: %s",
                    "Created" if created else "Updated",
                    obj.category_name
                )
            for p in products:
                obj, created = Product.objects.update_or_create(
                    sku=p["sku"],
                    is_deleted=False,
                    defaults={
                        "product_name": p["product_name"],
                        "product_description": p.get("product_description", ""),
                        "product_price": p["product_price"],
                        "currency": p["currency"],
                        "stock_quantity": p["stock_quantity"],
                        "image_url": p.get("image_url", ""),
                        "category_id": p["category_id"],
                    }
                )
                if created:
                    logger.info(f"Created product: {p['product_name']}")
                else:
                    logger.info(f"Updated product: {p['product_name']}")
    except Exception as e:
        logger.error(f"Error processing bulk upload: {str(e)}")
