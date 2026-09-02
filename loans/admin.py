import logging
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils import timezone
from .models import Loan

logger = logging.getLogger('django')


class OverdueFilter(admin.SimpleListFilter):
    title = 'Overdue Status'
    parameter_name = 'overdue'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Overdue (>14 Days) '),
        )


    def queryset(self, request, queryset):
        if self.value() == 'yes':
            fourteen_days_ago = timezone.now() - timezone.timedelta(days=14)
            return queryset.filter(status='BORROWED', borrow_date__lt=fourteen_days_ago)



@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('member', 'book', 'borrow_date', 'return_date', 'status_badge')
    list_filter = ('status', OverdueFilter, 'borrow_date')
    search_fields = ('member__username', 'book__title')
    readonly_fields = ('borrow_date',)
    fields = ('member', 'book', 'status', 'borrow_date', 'return_date')
    list_per_page = 10


    actions = ['mark_as_returned']

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.status == 'BORROWED':
            return mark_safe('<span style="background-color: #fff3cd; color: #856404; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 12px;">Active Loan 📖</span>')
        return mark_safe('<span style="background-color: #d4edda; color: #155724; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 12px;">Returned ✅</span>')

    @admin.action(description=' Mark selected loans as Returned')
    def mark_as_returned(self, request, queryset):
        count = 0
        for loan in queryset.filter(status='BORROWED'):
            loan.status = 'RETURNED'
            loan.return_date = timezone.now()
            loan.save()
            loan.book.available_copies += 1
            loan.book.save()
            count += 1
            
        
            logger.info(f"SECURITY AUDIT: Loan #{loan.id} ({loan.book.title}) marked as RETURNED by Admin '{request.user.username}'")

        self.message_user(request, f"Successfully returned {count} book(s)!")

    def save_model(self, request, obj, form, change):
        if not change:
            if obj.book.available_copies > 0:
                obj.book.available_copies -= 1
                obj.book.save()
                super().save_model(request, obj, form, change)
                logger.info(f"SECURITY AUDIT: New Loan #{obj.id} created for '{obj.member.username}' by Admin '{request.user.username}'")
        else:
            old_obj = Loan.objects.get(pk=obj.pk)
            if old_obj.status == 'BORROWED' and obj.status == 'RETURNED':
                if not obj.return_date:
                    obj.return_date = timezone.now()
                obj.book.available_copies += 1
                obj.book.save()
                
            super().save_model(request, obj, form, change)
            logger.info(f"SECURITY AUDIT: Loan #{obj.id} status changed to '{obj.status}' by Admin '{request.user.username}'")