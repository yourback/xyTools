from django.db import models


# Create your models here.
class Food(models.Model):
    # 食物分类
    FOOD_TYPES = (
        (0, '未分类'),
        (1, '主食'),
        (2, '蛋、肉、奶'),
        (3, '蔬菜、水果'),
        (4, '油、调味品'),
        (5, '零食、饮品'),
    )
    food_name = models.CharField(verbose_name='食物名称', max_length=20, unique=True)
    food_alias = models.CharField(verbose_name='食物别名', max_length=50)
    food_type = models.IntegerField(verbose_name='食物分类', choices=FOOD_TYPES)
    food_purine = models.IntegerField(verbose_name='食物嘌呤含量（毫克/100克）')
    food_calories = models.IntegerField(verbose_name='食物热量（大卡/100克）')
    food_carbohydrate = models.FloatField(verbose_name='食物碳水含量（克/100克）')
    food_protein = models.FloatField(verbose_name='食物蛋白质含量（克/100克）')
    food_fat = models.FloatField(verbose_name='食物脂肪含量（克/100克）')
    food_cellulose = models.FloatField(verbose_name='食物纤维素含量（克/100克）')
    food_description = models.CharField(verbose_name='食物描述', max_length=150)
    food_create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    food_is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        verbose_name_plural = '食物'

    def __str__(self):
        return self.food_name
