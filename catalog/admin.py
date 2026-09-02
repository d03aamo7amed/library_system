from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Book
admin.site.site_header = "Library Management Administration"
admin.site.site_title = "Library Admin Portal"
admin.site.index_title = "Welcome to Library Management System"
admin.site.site_url = "/admin/catalog/book/"

@admin.register(Book)

class BookAdmin(admin.ModelAdmin):
    list_display = ('cover_preview', 'title', 'author', 'category', 'total_copies', 'available_copies', 'status_badge')
    list_editable = ('available_copies',) 
    
    search_fields = ('title', 'author', 'isbn')

    search_help_text = "Search by Title, Author, or ISBN"
    list_filter = ('category',)
    ordering = ('title',)
    list_per_page = 10
    save_on_top = True 
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'author', 'isbn', 'category', 'cover')
        }),
        ('Inventory Management', {
            'fields': ('total_copies', 'available_copies'),
        }),
    )
    @admin.display(description='Cover')
    def cover_preview(self, obj):
        if obj.cover:
            return mark_safe(f'<img src="{obj.cover.url}" width="45" height="55" style="object-fit: cover; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.15);" />')
        return mark_safe('<span style="color: #999;">No Cover</span>')
    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.available_copies > 0:
            return mark_safe('<span style="background-color: #d4edda; color: #155724; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 12px; display: inline-block;">Available</span>')
        return mark_safe('<span style="background-color: #f8d7da; color: #721c24; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 12px; display: inline-block;">Out of Stock</span>')

    actions = ['add_one_copy', 'remove_one_copy']

    @admin.action(description='Add 1 copy to selected books')
    def add_one_copy(self, request, queryset):
        for book in queryset:
            book.total_copies += 1
            book.available_copies += 1
            book.save()
        self.message_user(request, "Successfully added 1 copy!")

    @admin.action(description='Remove 1 copy from selected books')
    def remove_one_copy(self, request, queryset):
        for book in queryset:
            if book.available_copies > 0:
                book.available_copies -= 1
                book.total_copies = max(0, book.total_copies - 1)
                book.save()
        self.message_user(request, "Successfully removed 1 copy!")