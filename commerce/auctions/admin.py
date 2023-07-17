from django.contrib import admin

from .models import User, Category, List, Bid, Comment

admin.site.register(User)
admin.site.register(Category)
admin.site.register(List)
admin.site.register(Bid)
admin.site.register(Comment)