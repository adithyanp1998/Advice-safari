from django.contrib import admin
from .models import Product
# Register your models here.
class productAdmin(admin.ModelAdmin):
    list_display=['title','description','price','category','image','created_at']


admin.site.register(Product,productAdmin)
