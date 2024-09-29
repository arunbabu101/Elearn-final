from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.

class CuricullamAdmin(admin.StackedInline):
    model = Curriculam
 
class featuresAdmin(admin.StackedInline):
    model = features

class faqAdmin(admin.StackedInline):
    model = faq






 



 
@admin.register(Curriculam)
class CuricullamAdmin(admin.ModelAdmin):
    pass

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


admin.site.register(Category)
admin.site.register(MainCourse)
admin.site.register(Customer)
admin.site.register(clients)
admin.site.register(subcat)
admin.site.register(ChatMessage)