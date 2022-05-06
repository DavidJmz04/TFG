from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Product, Bid, Picture, Profile

class PictureInline(admin.TabularInline):
    model = Picture

class BidInline(admin.TabularInline):
    model = Bid

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'quantity', 'measure', 'type', 'initial_bid', 'final_bid', 'origin', 'created_date', 'finished_date', 'seller']
    list_editable = ['quantity', 'measure', 'type', 'initial_bid', 'final_bid', 'origin', 'seller']
    list_filter = ['measure', 'type', 'origin']
    search_fields = ['title']
    inlines = [PictureInline, BidInline]

class ProfileInline(admin.TabularInline):
    model = Profile
    can_delete = False

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.register(Product, ProductAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)