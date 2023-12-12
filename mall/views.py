# django import
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView # django Pasination을 위해 ListView를 사용합니다. ListView는 페이징 기능을 제공합니다.(23.12.10)
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib import messages
# local import
from .models import CartProduct, Product
from .forms import CartProductForm

# Create your views here.
"""
def product_list(request):
    products_qs = Product.objects.all().select_related("category")
    product_category = request.GET.get('product_category')
    # Product 에서 Category를 외래키로 참조해서 가져오는 것은, 데이터베이스에 쿼리를 두번 요청하는 것이므로 비효율적입니다. 이를 해결하기 위해 select_related() 메서드를 사용합니다.
    return render(
        request,
        'mall/product_list.html',
        {
            "product_list": products_qs,
            "product_category": product_category,
        },
    )
"""

class ProductListView(ListView):
    # ListView에서는 template_name을 지정하지 않으면, 자동으로 모델명_list.html을 찾습니다.
    # ListView에서는 "product_list" 라는 이름으로 context를 만듭니다.
    model = Product
    queryset = Product.objects.filter(status=Product.Status.ACTIVE).select_related("category") # 정적으로 쿼리셋 지정
    paginate_by = 6

    def get_queryset(self): # 동적으로 쿼리셋 지정
        qs =  super().get_queryset()
        query = self.request.GET.get("query", "")
        if query:
            qs = qs.filter(name__icontains=query)
        return qs

product_list = ProductListView.as_view()
# http://127.0.0.1:8000/mall/?page=2 라고쓰면 2 페이지로 이동합니다.


@login_required
def add_to_cart(request, product_pk):
    product_qs = Product.objects.filter(
        status=Product.Status.ACTIVE
        )
    product = get_object_or_404(product_qs, pk=product_pk) # Active가 아닌 상품은 장바구니에 담을 수 없도록 합니다.
    quantity = int(request.POST.get("quantity", 1)) # quantity가 없으면 1로 지정합니다.
    cart_product, is_created = CartProduct.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": quantity},
    )
    if not is_created: # 장바구니에 이미 담긴 상품일 경우, 추가로 담습니다.
        cart_product.quantity += quantity
        cart_product.save()

    messages.success(request, f"{product.name}을 장바구니에 담았습니다.")

    return redirect("product_list")


@login_required
def cart_detail(request):
    cart_product_qs = CartProduct.objects.filter(
        user=request.user,
        ).select_related("product").order_by("product__name")
        # select_related() 메서드를 사용해서, product를 미리 가져옵니다.
        # 가나다순으로 정렬.
    CartProductFormSet = modelformset_factory(
        model=CartProduct,
        form=CartProductForm,
        can_delete=True,
    )

    if request.method == "POST":
        formset = CartProductFormSet(
            data=request.POST,
            queryset=cart_product_qs,
            )
        if formset.is_valid():
            formset.save()
            messages.success(request, "장바구니를 수정했습니다.")
            return redirect("cart_detail")
    else:
        formset = CartProductFormSet(
            queryset=cart_product_qs,
        )

    return render(
        request,
        "mall/cart_detail.html",
        {
        "formset": formset,
        },
    )
    # 1개의 인스턴스 수정은 장고 ModelForm을 사용하지만, 다수의 인스턴스를 수정할 때는 ModelFormSet을 사용합니다. (23.12.12)
