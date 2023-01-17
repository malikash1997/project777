from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Course)
admin.site.register(models.Cart)
admin.site.register(models.Cabinet)
admin.site.register(models.Sale)
admin.site.register(models.Programs)
admin.site.register(models.CourseLevel)
