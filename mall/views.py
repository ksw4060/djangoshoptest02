# django import
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.forms import modelformset_factory
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.views.generic import ListView # django Pasination을 위해 ListView를 사용합니다. ListView는 페이징 기능을 제공합니다.(23.12.10)
# local import
from .models import CartProduct, Product, Order, OrderPayment
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
@require_POST
def add_to_cart(request, product_pk):
    product_qs = Product.objects.filter(
        status=Product.Status.ACTIVE,
    )
    product = get_object_or_404(product_qs, pk=product_pk)
    quantity = int(request.GET.get("quantity", 1))
    cart_product, is_created = CartProduct.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": quantity},
    )
    if not is_created:
        cart_product.quantity += quantity
        cart_product.save()

     # HTTP_REFERER는 이전 페이지의 URL을 가져옵니다. 브라우저의 기능입니다. HTTP_REFERER가 없으면 product_list를 보여줍니다 (23.12.13)
    # redirect_url = request.META.get("HTTP_REFERER", "product_list")
    # return redirect(redirect_url)
    # <장바구니 담기는, POST 만 가능하기 때문에, redirect는 사용하지 않습니다. (23.12.13)>
    return HttpResponse("장바구니에 담았습니다.")


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
        extra=0, # 추가로 폼을 생성하지 않습니다.
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

@login_required
def order_new(request):
    cart_product_qs = CartProduct.objects.filter(user=request.user)

    order = Order.create_from_cart(request.user, cart_product_qs)
    cart_product_qs.delete()

    return redirect("order_pay", order.pk)


@login_required
def order_pay(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if not order.can_pay():
        messages.error(request, "현재 결제를 할 수 없는 주문입니다.")
        return redirect("order_detail", order.pk)
        # TODO: order_detail 구현

    payment = OrderPayment.create_by_order(order)

    payment_props = {
        "merchant_uid": payment.merchant_uid,
        "name": payment.name,
        "amount": payment.desired_amount,
        "buyer_name": payment.buyer_name,
        "buyer_email": payment.buyer_email,
    }
    return render(
        request,
        "mall/order_pay.html",
        {
            "portone_shop_id": settings.PORTONE_SHOP_ID,
            "payment_props": payment_props,
            "next_url": reverse("order_check", args=[order.pk, payment.pk]),
        },
    )


@login_required
def order_check(request, order_pk, payment_pk):
    payment = get_object_or_404(OrderPayment, pk=payment_pk, order__pk=order_pk)
    payment.update()
    # TODO: 업데이트를 해야합니다.

    return redirect("order_detail", order_pk)
