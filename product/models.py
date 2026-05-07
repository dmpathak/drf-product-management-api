from django.db import models
from django.db.models import Q


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = ActiveManager()  # default → only active
    all_objects = models.Manager()  # includes deleted

    class Meta:
        abstract = True


class Category(BaseModel):
    category_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.category_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category_name'],
                condition=Q(is_deleted=False),
                name='unique_category_name'
            )
        ]


class Product(BaseModel):
    product_description = models.TextField()
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="INR")
    stock_quantity = models.IntegerField()
    sku = models.CharField(max_length=20)
    image_url = models.URLField()

    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products')

    def __str__(self):
        return f"{self.category} - {self.product_name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sku'],
                condition=Q(is_deleted=False),
                name='unique_active_sku'
            )
        ]
