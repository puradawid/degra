from django.contrib import admin
from apps.plan.models import Teacher, Course, Group, Lesson, Post

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'email',)
    search_fields = ['name', 'surname',]

admin.site.register(Teacher, TeacherAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ['name',]
    
admin.site.register(Course, CourseAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ['field_of_study', 'semestr', 'name',]
    list_filter = ('field_of_study', 'semestr',)
    
admin.site.register(Group, GroupAdmin)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ['course', 'group',]

admin.site.register(Lesson, LessonAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    search_fields = ['title',]
    list_filter = ('created',)

admin.site.register(Post, PostAdmin)