from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Product, Bid, Picture, Profile

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'type', 'initial_bid', 'final_bid', 'origin', 'created_date', 'finished_date', 'seller']
    list_editable = ['type', 'initial_bid', 'final_bid', 'origin', 'seller']
    list_filter = ['type', 'origin']
    search_fields = ['title']

class BidAdmin(admin.ModelAdmin):
    list_display = ['price', 'created_date', 'product', 'buyer']
    list_editable = ['product']
    list_filter = ['product', 'buyer']

class PictureAdmin(admin.ModelAdmin):
    list_display = ['image', 'product']
    list_editable = ['product']
    list_filter = ['product']

# Define an inline admin descriptor for Profile
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.register(Product, ProductAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Picture, PictureAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)