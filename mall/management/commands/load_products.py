from dataclasses import dataclass

import requests
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from tqdm import tqdm

from mall.models import Category, Product

# https://raw.githubusercontent.com/pyhub-kr/dump-data/main/django-shopping-with-iamport/product-list.json
BASE_URL = "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/django-shopping-with-iamport/"


@dataclass # dataclass 데코레이터를 사용하면 클래스를 정의할 때, __init__ 메서드를 자동으로 생성해준다.
class Item:
    category_name : str
    name : str
    price : int
    priceUnit : str
    desc : str
    photo_path : str



class Command(BaseCommand):
    help = "Load products from JSON file."
    # handle 메서드는 BaseCommand 클래스에 구현되어 있는 메서드이다.
    # Command 를 호출하면 handle 메서드가 자동 실행된다.
    def handle(self, *args, **options):
        json_url = BASE_URL + "product-list.json"
        item_dict_list = requests.get(json_url).json()

        item_list = [Item(**item_dict) for item_dict in item_dict_list]
        category_name_set = {item.category_name for item in item_list}

        category_dict = {}
        for category_name in category_name_set:
            category, __ = Category.objects.get_or_create(name=category_name or "미분류")
            # print(category_name)
            category_dict[category.name] = category
            print(category_dict)
        # print(category_dict)
        for item in tqdm(item_list):
            category: Category = category_dict[item.category_name or "미분류"]
            product, is_created = Product.objects.get_or_create(
                category=category,
                name=item.name,
                defaults={
                    "description": item.desc,
                    "price": item.price,
                },
            )
            if is_created:
                photo_url = BASE_URL + item.photo_path
                filename = photo_url.rsplit("/", 1)[-1]
                photodata = requests.get(photo_url).content # image 를 서버로부터 받아오는 것은 부하가 크기 때문에, raw data 를 받아온다.
                product.photo.save(
                    name=filename,
                    content=ContentFile(photodata),
                    save=True,
                )
                # raw data
        """
        for item in tqdm(item_list):
            category: Category = category_dict[item.category_name or "미분류"]
            product, is_created = Product.objects.get_or_create(
                category=category,
                name=item.name,
                defaults={
                    "description": item.desc,
                    "price": item.price,
                },
            )
            if is_created:
                photo_url = BASE_URL + item.photo_path
                filename = photo_url.rsplit("/", 1)[-1]
                photo_data = requests.get(photo_url).content  # raw data
                product.photo.save(
                    name=filename,
                    content=ContentFile(photo_data),
                    save=True,
                )
        """



        """
        for item_dict in item_dict_list:
            item = Item(**item_dict) # item_dict 를 Item 클래스의 인스턴스로 만들어준다.
            print(item)
            item_list.append(item)
        # list comprehension 을 사용하면
        # item_list = [Item(**item_dict) for item_dict in item_dict_list] 이 된다
        """
