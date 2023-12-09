from django.shortcuts import render
from .models import Product

# Create your views here.
def product_list(request):
    # products_qs = Product.objects.all()
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
