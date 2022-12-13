from django.contrib import admin

# Register your models here.
from .models import Dealer
from .models import Product
from .models import Promotion
from .models import order
from .models import dealer_code

admin.site.register(Dealer)

admin.site.register(Product)

admin.site.register(Promotion)

admin.site.register(order)

admin.site.register(dealer_code)