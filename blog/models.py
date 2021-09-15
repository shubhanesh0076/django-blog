#from _typeshed import Self
from enum import unique
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.timezone import now
import numpy as np
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.



class Add_Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    category_name=models.CharField(max_length=255)
    slug_cat=models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return (self.category_name)

    def get_absolute_url(self):
        kwargs = {
            'id': self.cat_id,
            'slug': self.slug_cat
        }
        return reverse('filterpost', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.category_name
        self.slug_cat = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
    

STATUS = (
    ('0','Draft'),
    ('1','Publish'),
    ('2','Withdrawn'),
)

class Post(models.Model):
    title = models.CharField(max_length=200)
    title_tag = models.CharField(max_length=200,  null=True, blank=True)
    category = models.ForeignKey(Add_Category, on_delete=models.CASCADE, related_name="blog_category", null=True, blank=True)
    bannerimage = models.FileField(null=True, blank=True, upload_to="images/")
    thumbnailimg = models.ImageField(null=True, blank=True, upload_to="thumbnailimg/")
    slug = models.SlugField(max_length=200, unique=True)
    user_id = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_post', null=True)
    updated_on = models.DateTimeField(auto_now= True)
    content = RichTextUploadingField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, default=0, max_length=10)
    #snippets = models.CharField(max_length=200, default="Give the snapshot to blog. ", null=True, blank=True)
    likes = models.ManyToManyField(User, default=None, blank=True, related_name="likes")
    view = models.IntegerField(default=0)
    view_post_bool = models.BooleanField(default=False)


    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    

    def total_views(self):
        return self.view.count()

    def total_likes(self):
        return self.likes.count()


    def get_absolute_url(self):
        kwargs = {
            'id': self.id,
            'slug': self.slug
        }
        return reverse('model_detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)



    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        return np.mean(all_ratings)
        
    def __unicode__(self):
        return self.title

        



CHOOSE_BOOL = (
     ("True","True"),
     ("False","False")
)
class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    post_bool = models.CharField(choices=CHOOSE_BOOL, default=False, max_length=10)
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        return self.comment
    class Meta:
        ordering = ['-timestamp']

# CHOOSE_LIKE = (
#     ("like","like"),
#     ("unlike","unlike")
# )

class Bloglikes(models.Model):
    sno = models.AutoField(primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    #comment=models.OneToOneField(BlogComment, on_delete=models.CASCADE)
    #values = models.CharField(choices=CHOOSE_LIKE, default="like", max_length=10)
    #parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['-timestamp']
    



    

class Contact(models.Model):
    id= models.AutoField(primary_key=True)
    name= models.CharField(max_length=255)
    email= models.CharField(max_length=100)
    contact= models.CharField(max_length=13)
    content= models.TextField()
    timeStamp=models.DateTimeField(auto_now_add=True)

    class Mets:
        ordering=['-timeStamp']

    def __str__(self):
        return self.name
    

gender = (
        ("M", "Male"),
        ("F", "Female"),
    )



class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    userprofileimg=models.ImageField(upload_to="profileimage/", default="profileimage/einstein.png")
    userbannerimage=models.ImageField(upload_to="userbannerimage/", default="userbannerimage/1543903484career-launcher-logo.png")
    #datetime=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"

    
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Userprofile.objects.create(user=instance)
    post_save.connect(create_user_profile, sender=User)

    
class Profileinfoform(models.Model):
    puser = models.OneToOneField(User, on_delete=models.CASCADE)
    #puser = models.CharField(default="qwd", max_length=10)
    name=models.CharField(max_length=50, null=True)
    middlename=models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=150, null=True)
    phoneno1 = models.CharField(max_length=13, null=True)
    phoneno2 = models.CharField(max_length=13, null=True)
    gender = models.CharField(choices=gender, max_length=7)
    address = models.CharField(max_length=250, null=True)
    permanentaddress = models.CharField(max_length=250, null=True)
    country = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    pincode=models.IntegerField(null=True)
    dob = models.DateField(null=True)
    updated_on = models.DateField(auto_now_add=True)
    about = models.CharField(max_length=250, null=True) 
    
    university = models.CharField(max_length=150, null=True)
    startdate = models.DateField(null = True)
    completiondate = models.DateField(null = True)
    unicity = models.CharField(max_length=30, null=True)

    college = models.CharField(max_length=150, null=True)
    collegestartdate = models.DateField(null = True)
    collegecompletiondate = models.DateField(null = True)
    collegecity = models.CharField(max_length=30, null=True)

    school = models.CharField(max_length=150, null=True)
    schoolstartdate = models.DateField(null = True)
    schoolcompletiondate = models.DateField(null = True)
    schoolcity = models.CharField(max_length=30, null=True)

    company = models.CharField(max_length=30, null=True)
    experience = models.IntegerField(default=0, null=True)
    companycity = models.CharField(max_length=30, null=True)
    technicalskills = models.CharField(max_length=200,null=True)
    hobbies = models.CharField(max_length=200, null=True)
    abouthobbies = models.CharField(max_length=200, null=True)
    
    website = models.CharField(max_length=150, null=True)
    facebook = models.CharField(max_length=100, null=True)
    twitter = models.CharField(max_length=100, null=True)
    youtube = models.CharField(max_length=100, null=True)
    linkedin = models.CharField(max_length=100, null=True)


    def __str__(self):
        return self.puser

    def create_user_profileinfoform(sender, instance, created, **kwargs):
        if created:
            Profileinfoform.objects.create(puser=instance)
    post_save.connect(create_user_profileinfoform, sender=User)




class Reviews(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    user_name = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True,blank=True)
    review = models.TextField(max_length=250, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} rate us {self.rating} " 

    class Meta:
        verbose_name_plural='Reviews'

    def get_review_rating(self):
        return self.rating
        


