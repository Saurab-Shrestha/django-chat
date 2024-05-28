from django.contrib import admin, sites
from chat.models import MessageModel
# Register your models here.

class MessageModelAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)
    search_fields = ('id', 'body', 'user__email', 'recipient__email')
    list_display = ('id', 'user', 'recipient', 'timestamp', 'characters')
    list_display_links = ('id',)
    list_filter = ('user', 'recipient')
    date_hierarchy = 'timestamp'

admin.site.register(MessageModel, MessageModelAdmin)
