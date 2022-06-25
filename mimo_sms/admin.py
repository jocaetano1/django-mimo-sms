from django.contrib import admin, messages

from mimo_sms.api import MimoSender

from .forms import CreditForm
from .models import (
    Recipient,
    Activity,
    Message,
    Sender,
)


class RecipentInline(admin.StackedInline):
    model = Recipient
    fields = ('phone',)
    min_num = 1
    max_num = 20


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    autocomplete_fields = ('sender',)
    fieldsets = (
        ('Sender MIMO', {'fields': ('sender',)}),
        ('Message', {'fields': ('text',)})
    )
    list_display = (
        'id', 'sender', 'view_message_id',
        'text', 'unicode', 'size')
    list_filter = ('unicode',)
    list_per_page = 25
    list_display_links = ('sender', 'text')
    search_fields = ('sender', 'message_id')
    inlines = (RecipentInline,)
    ordering = ('-create_at',)

    def view_message_id(self, message_obj):
        return message_obj.message_id

    def save_model(self, request, obj, form, change) -> None:
        return super().save_model(request, obj, form, change)

    def has_add_permission(self, *args) -> bool:
        return False

    def has_delete_permission(self, *args) -> bool:
        return False

    def has_change_permission(self, *args) -> bool:
        return False

    def has_delete_permission(self, *args) -> bool:
        return False

    view_message_id.short_description = 'message Id'


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    autocomplete_fields = ('message',)
    list_display = ('phone', 'messageId', 'status')
    list_select_related = ('message',)
    list_per_page = 25
    readonly_fields = ('message', 'phone', 'messageId', 'status')

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, *args) -> bool:
        return False

    def has_delete_permission(self, *args) -> bool:
        return False


@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    fields = ('sender', 'reason')
    list_filter = ('status', 'default')
    list_display = ('sender', 'status', 'reason', 'view_hours')
    search_fields = ('sender',)
    actions = ['check_senders']

    def view_hours(self, sender):
        if not sender.status:
            return "48h"
        return "-"

    def save_model(self, request, obj, form, change) -> None:
        sender = form.cleaned_data.get('sender')
        reason = form.cleaned_data.get('reason')
        sender_obj = MimoSender()
        sender_obj.create(sender=sender, reason=reason)
        return super().save_model(request, obj, form, change)

    @admin.action(description='Check sender availability')
    def check_senders(self, request, queryset):
        sender_obj = MimoSender()
        res = sender_obj.list()
        senders = res.get('content')
        senders_enable = []
        for sender in senders:
            if sender['status'] == "enable":
                senders_enable.append(sender.get('sender'))
        queryset_1 = queryset.filter(sender__in=senders_enable)
        if queryset_1:
            updated = queryset_1.update(status=Sender.Status.ENABLE)
            self.message_user(
                request, "All senders have been verified", updated, messages.SUCCESS)
        else:
            self.message_user(
                request, "Unable to check sender availability", level=messages.ERROR)

    def has_delete_permission(self, *args) -> bool:
        return False

    def has_change_permission(self, *args) -> bool:
        return False

    view_hours.short_description = 'Hours to check'


@ admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    form = CreditForm
    fields = ('voucher',)
    list_display = (
        'serial_number', 'voucher', 'view_type',
        'credits', 'view_price', 'status')

    def has_change_permission(self, *args) -> bool:
        return False

    def view_price(self, activity):
        return activity.price_format

    def view_type(self, activity):
        return activity.get_type_display()

    view_price.short_description = 'price'
    view_type.short_description = 'Type'
