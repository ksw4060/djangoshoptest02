from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator

# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "상품 분류"

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"



class Product(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "활성화"
        SOLDOUT = "soldout", "품절"
        OBSOLETE = "obsolete", "단종"
        INACTIVE = "inactive", "비활성화"
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_constraint=False) # db_constraint=False 는 외래키 제약조건을 걸지 않겠다는 의미
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField() # 0 이상의 정수
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.INACTIVE)
    photo = models.ImageField(blank=True, upload_to="mall/product/photo/%Y/%m/%d")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<{self.id}: {self.name}>"
    class Meta:
        verbose_name = verbose_name_plural = "상품"
        ordering = ["-pk"] # default는 -pk 이고, 다른 정렬을 원하면 views에서 order_by를 사용하면 됩니다.


class CartProduct(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        db_constraint=False,
        related_name="cart_product_set",
        )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_constraint=False,
        )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
        ],
        )

    def __str__(self):
        return f"<{self.pk}> : {self.product.name} - {self.quantity}>"
    class Meta:
        verbose_name = verbose_name_plural = "장바구니 상품"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product",
            ),
        ]
