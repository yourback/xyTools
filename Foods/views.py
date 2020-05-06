import re
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse

import Foods
from .models import Food


# Create your views here.

def get_food_info(request, food_name):
    # food_info = get_food_info_internet(food_name)
    # print(food_info)
    # return HttpResponse(food_info.__str__())

    # 检索数据库中是否有数据
    try:
        food = Food.objects.get(food_name=food_name)
        return HttpResponse(food.__str__())
    except ObjectDoesNotExist or Foods.models.Food.DoesNotExist:
        # 若没有则去网络中去查询
        food_info = get_food_info_internet(food_name)
        print(food_info)
        # 添加到数据库中
        Food.objects.update_or_create(
            food_name=food_info['name'],
            food_alias=food_info['food_alias'],
            food_type=food_info['food_type'],
            food_purine=food_info['food_purine'],
            food_calories=food_info['food_calories'],
            food_carbohydrate=food_info['food_carbohydrate'],
            food_protein=food_info['food_protein'],
            food_fat=food_info['food_fat'],
            food_cellulose=food_info['food_cellulose'],
            food_description=food_info['food_description'],
        )
        return HttpResponse(food_info.__str__())


# 爬虫爬取相关数据筛选后
def get_food_info_internet(food_name):
    print('爬取' + food_name + '相关数据')
    base_url = 'https://www.boohee.com/'
    url = 'https://www.boohee.com/food/search?keyword=' + food_name
    r = requests.get(url)
    error_text = '抱歉，没有找到'
    if error_text in r.text:
        return '没有找到相关信息'
    # 如果不是空，应该是第一个item的网址
    result = re.search('text-box pull-left.*?href="(.*?)" title', r.text, re.S)
    url_next = base_url + result.group(1)
    r = requests.get(url_next)
    name = re.search(
        '<title>(.*?)的热量.*? - 薄荷食物库</title>', r.text,
        re.S).group(1)
    food_alias = re.search('ul.*?basic-infor.*?<b>别名：</b>(.*?)<', r.text, re.S)
    if food_alias:
        food_alias = food_alias.group(1)
    else:
        food_alias = ''
    if any(food_name.endswith(key) for key in ['肉', '蛋', '奶']):
        food_type = 2
    elif food_name.endswith('菜'):
        food_type = 3
    else:
        food_type = 0
    food_calories = re.search(r'span.*?stress red1.*?>(.*?)<', r.text, re.S).group(1)
    food_carbohydrate = float(re.search(r'碳水化合物\(克\).*?<span class="dd">(.*?)</span>', r.text, re.S).group(1))
    food_protein = float(re.search(r'<span class="dt">蛋白质.*?"dd">(.*?)<', r.text, re.S).group(1))
    food_fat = float(re.search(r'<span class="dt">脂肪.*?"dd">(.*?)<', r.text, re.S).group(1))
    food_cellulose = re.search(r'<span class="dt">纤维素.*?"dd">(.*?)<', r.text, re.S).group(1)
    if "一" in food_cellulose:
        food_cellulose = float(0)
    food_description = re.search(r'<b>评价：</b>(.*?)\n', r.text, re.S).group(1)
    # get food_purine
    food_purine = 0

    food_info = {'name': name,
                 'food_alias': food_alias,
                 'food_type': food_type,
                 'food_purine': food_purine,
                 'food_calories': food_calories,
                 'food_carbohydrate': food_carbohydrate,
                 'food_protein': food_protein,
                 'food_fat': food_fat,
                 'food_cellulose': food_cellulose,
                 'food_description': food_description
                 }
    return food_info
