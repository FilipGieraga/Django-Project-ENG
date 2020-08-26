from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.


admin.site.site_header = "Library Admin"
admin.site.site_title = "Library Admin Portal"
admin.site.index_title = "Welcome to Library Aministration Panel"

@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Person)
admin.site.register(Borrowed)