from rest_framework import serializers
from sales.models import order

class orderSerializer(serializers.ModelSerializer):
    class Meta:
        model = order
        fields = ['id','product', 'p_name', 'UOM', 'tp', 'order_qty', 'bonus_qty', 'balance']




