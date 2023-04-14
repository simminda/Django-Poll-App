from django.contrib import admin
from .models import Post, Question, Choice

# Registering models
admin.site.register(Question)
admin.site.register(Choice)

# Legacy content
admin.site.register(Post)


