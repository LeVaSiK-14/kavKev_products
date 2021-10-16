from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver



User = get_user_model()



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
    amount = models.PositiveIntegerField(
                                        default=0,
                                        verbose_name='Количество продукта в наличае',
                                        null=True)
    price = models.PositiveIntegerField(
                                    default= 0,
                                    verbose_name='Цена продукта')
    inStock = models.BooleanField(
                                default=True,
                                verbose_name='В наличае')
    articul = models.CharField(
                                max_length=127,
                                verbose_name='Артикул')
    raiting_general = models.DecimalField(
                                        max_digits=3,
                                        decimal_places=1,
                                        null=True,
                                        default=0.0,
                                        verbose_name='Рейтинг продукта')

    def __str__(self):
        return f'{self.category.category} - {self.name_product}'

    # class Meta:
    #     ordering = ['-raiting_general', ]
        

class RaitingStar(models.Model):
    value = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.value}'


class Raiting(models.Model):

    appraiser = models.ForeignKey(
                                User, 
                                on_delete=models.CASCADE, 
                                verbose_name='Оценщик')

    star = models.ForeignKey(
                            RaitingStar,
                            on_delete=models.CASCADE,
                            verbose_name='Количество звезд',
                            related_name='raitings')

    product = models.ForeignKey(
                                Products,
                                on_delete=models.CASCADE,
                                verbose_name='Продукт',
                                related_name='raitings')

    def __str__(self):
        return f'{self.star.value} + {self.product.name_product}'



class Cart(models.Model):
    
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    cart_product = models.ManyToManyField(Products, through='CartProduct')
    sum_price = models.PositiveIntegerField(default=0)




class CartProduct(models.Model):

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity_product = models.PositiveIntegerField(default=0)
    general_price = models.PositiveIntegerField(default=0)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        SUCCSESS = 'Успешно доставлен'
        IN_PENDING = 'В ожидании доставки'
        CANCELED = 'Отменён'

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order')
    created_at = models.DateTimeField(default=timezone.now)
    adress = models.CharField('Адрес', max_length=255)
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.SUCCSESS)

    def __str__(self):
        return f'{self.customer.username} - {self.adress}'

@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(customer=instance)
