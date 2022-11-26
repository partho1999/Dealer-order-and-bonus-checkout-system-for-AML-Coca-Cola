from django.contrib import admin

# Register your models here.
from .models import Dealer
from .models import Product
from .models import Promotion
from .models import order

admin.site.register(Dealer)

admin.site.register(Product)

admin.site.register(Promotion)

admin.site.register(order)