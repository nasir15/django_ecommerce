from django.contrib import admin
from .models import User,Product,Category,AdditionalImage,Person,Passport

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(AdditionalImage)
admin.site.register(Person)
admin.site.register(Passport)