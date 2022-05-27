from main.models import Like, Quote, Records, User
from django.contrib import admin

# Register your models here.
admin.site.register(User)
admin.site.register(Like)
admin.site.register(Quote)
admin.site.register(Records)
