from django.shortcuts import render
from .models import Product
from django.views.generic import ListView # django Pasination을 위해 ListView를 사용.
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
    queryset = Product.objects.all().select_related("category")
    paginate_by = 4

product_list = ProductListView.as_view()
# http://127.0.0.1:8000/mall/?page=2 라고쓰면 2 페이지로 이동합니다.
