from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission
from api.models import User, Product
from django.contrib.auth import get_user_model


seller_group, _ = Group.objects.get_or_create(name='Seller')
content_type = ContentType.objects.get_for_model(Product)
seller_permissions = Permission.objects.filter(content_type=content_type)
seller_group.permissions.set(seller_permissions)

sellers = User.objects.filter(user_type='SEL')
for seller in sellers:
    seller.groups.add(seller_group)

