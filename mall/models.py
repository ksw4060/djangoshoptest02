from django.db import models

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
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, db_constraint=False) # db_constraint=False 는 외래키 제약조건을 걸지 않겠다는 의미
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField() # 0 이상의 정수
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.INACTIVE, max_length=8)
    photo = models.ImageField(blank=True, upload_to="mall/product/photo/%Y/%m/%d")


    def __str__(self):
        return f"<Product {self.id}: {self.name}>"
    class Meta:
        verbose_name = verbose_name_plural = "상품"
        ordering = ["-id"]
