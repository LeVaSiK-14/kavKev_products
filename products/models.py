from django.db import models

class Category(models.Model):
    category = models.CharField(
                                max_length=127, 
                                default='')

    def __str__(self):
        return self.category

class Products(models.Model):
    category = models.ForeignKey(
                                Category,
                                on_delete=models.PROTECT,
                                related_name='products',
                                verbose_name='Категория продукта')
    name_product = models.CharField(
                                    max_length=255,
                                    verbose_name='Наименование продукта')
    composition = models.CharField(
                                    max_length=1027,
                                    verbose_name='Состав')
    price = models.PositiveIntegerField(
                                    verbose_name='Цена продукта')
    inStock = models.BooleanField(
                                default=True,
                                verbose_name='В наличае')
    articul = models.CharField(
                                max_length=127,
                                verbose_name='Артикул')

    def __str__(self):
        return self.category.category + self.name_product
        


