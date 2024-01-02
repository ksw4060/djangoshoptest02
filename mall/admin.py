from django.contrib import admin
from .models import Category, Product

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "status", "created_at", "updated_at"]
    list_display_links = ["name"]
    search_fields = ["name"]
    list_filter = ["category", "status", "created_at", "updated_at"]
    actions = ["make_active", "make_inactive"]

    @admin.action(description=f"{Product.Status.ACTIVE.label} 처리")
    def make_active(self, request, queryset):
        updated_count = queryset.update(status=Product.Status.ACTIVE)
        self.message_user(request, f"{updated_count}건의 상품을 활성화 상태로 변경했습니다.")

    @admin.action(description=f"{Product.Status.INACTIVE.label} 처리")
    def make_inactive(self, request, queryset):
        updated_count = queryset.update(status=Product.Status.INACTIVE)
        self.message_user(request, f"{updated_count}건의 상품을 비활성화 상태로 변경했습니다.")
