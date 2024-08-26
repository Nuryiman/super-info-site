from django.contrib import admin

from news.models import Publication, PublicationComment, Hashtag, Category, SocialNetwork, Address, ContactUs


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(PublicationComment)
class PublicationCommentAdmin(admin.ModelAdmin):
    list_display = ['publication', 'name', 'text']

    def has_add_permission(self, request,  obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ['instagram', 'facebook', 'twitter', 'youtube']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['address', 'phone', 'email', 'last_text']


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject']

    def has_add_permission(self, request,  obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
