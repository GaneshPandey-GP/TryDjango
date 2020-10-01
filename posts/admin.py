from django.contrib import admin
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title","update","timestamp"]
    list_filter=["timestamp"]
   
    class Meta:
        model = Post
        filds="__all__"

admin.site.register(Post,PostModelAdmin)