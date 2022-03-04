from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Cart, DeliveryCost

admin.site.register(User, UserAdmin)
admin.site.register(Cart)
admin.site.register(DeliveryCost)
