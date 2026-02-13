from django.contrib import admin
from translation.models import PaymentProfile, HourlyPricing
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from translation.models import Transaction, ShareCode, Usage, Contact, TranscriptRecord
from django.contrib import admin

class PaymentProfileInline(admin.StackedInline):
    model = PaymentProfile
    can_delete = False
    verbose_name_plural = "payment_profile"

class UserAdmin(BaseUserAdmin):
    inlines = [PaymentProfileInline]

@admin.register(HourlyPricing)
class HourlyPricingAdmin(admin.ModelAdmin):
    list_display = ('price',)
    fields = ('price',)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company_name', 'company_size', 'created_at')
    list_filter = ('company_size', 'created_at')
    search_fields = ('name', 'company_name', 'email')
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Contact, ContactAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Transaction)
admin.site.register(ShareCode)
admin.site.register(Usage)
admin.site.register(TranscriptRecord)

