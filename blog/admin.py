from django.contrib import admin
from django.contrib.auth import models
from .models import Add_Category ,Bloglikes, Post, Contact, BlogComment, Profileinfoform, Reviews, Userprofile

# Register your models here..!

class PostAdmin(admin.ModelAdmin):
   list_display = ('id','title', 'status','created_on','bannerimage', 'thumbnailimg')
   # list_filter = ("status",)
    #search_fields = ['title', 'content']
    #prepopulated_fields = {'slug': ('title',)}


class ReviewAdmin(admin.ModelAdmin):
    model = Reviews
    list_display = ('id', 'user_name', 'post', 'review', 'rating',  'pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['review']
    
class LikesAdmin(admin.ModelAdmin):
    model=Bloglikes
    list_display=('sno', 'user', 'post', 'timestamp')
    #list_filter=['user', 'timestamp']

class BlogCommentAdmin(admin.ModelAdmin):
    model=BlogComment
    list_display=('sno', 'comment', 'user', 'post', 'parent', 'timestamp')

class UserprofileAdmin(admin.ModelAdmin):
    model = Userprofile
    list_display=['user', 'userprofileimg', 'userbannerimage']

class AddCatAdmin(admin.ModelAdmin):
    model=Add_Category
    list_display = ('cat_id', 'category_name')




admin.site.register(Post, PostAdmin)
admin.site.register(Contact)
admin.site.register(BlogComment, BlogCommentAdmin)
admin.site.register(Bloglikes, LikesAdmin)
admin.site.register(Profileinfoform)
admin.site.register(Reviews, ReviewAdmin)
admin.site.register(Userprofile, UserprofileAdmin)
admin.site.register(Add_Category, AddCatAdmin)










    






