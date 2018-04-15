from django.contrib import admin

from .models import Order_Details, Order_Item_Detail


admin.site.register(Order_Details)
admin.site.register(Order_Item_Detail)

# Register your models here.
