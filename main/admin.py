from django.contrib import admin
from .models import Log,Department,Out, Document_type
from django.template.defaultfilters import truncatewords
import csv
from django.http import HttpResponse

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"



@admin.register(Department)
class DepartmentsOf(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id','name')
    list_filter = ('id', 'name');
    search_fields = (
        'id', 'name'
    );
    actions = ["export_as_csv"]


@admin.register(Document_type)
class DocumentsOf(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id','name')
    list_filter = ('id', 'name');
    search_fields = (
        'id', 'name'
    );
    actions = ["export_as_csv"]

