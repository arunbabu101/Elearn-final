from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import time
import os
from edureka import settings

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='media/profile_pic',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    Country = models.CharField(max_length=20,null=False, blank=True)
    Company = models.CharField(max_length=20,null=False, blank=True)
    City =  models.CharField(max_length=20,null=False, blank=True)
    State =  models.CharField(max_length=20,null=False, blank=True)
    Zip_Code =  models.IntegerField(blank=True, default="1")
    Telephone =  models.IntegerField(blank=True, default="1")
    Extension =  models.CharField(max_length=20,null=False, blank=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name

class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank = True, null=True)
    title = models.CharField(max_length=100) 
    slug = AutoSlugField(populate_from='title', unique=True, null=False, editable=True)
    logo = models.ImageField(upload_to='media/catlogo', blank=True, null=True, help_text='Optional')
    logo1 = models.ImageField(upload_to='media/catlogo', blank=True, null=True, help_text='Optional')
    logo2 = models.ImageField(upload_to='media/catlogo', blank=True, null=True, help_text='Optional')
    top_three_cat = models.BooleanField(default=False)
    more = models.BooleanField(default=False, blank=True, verbose_name="For Add In Right Menu")
    created_at = models.DateTimeField(auto_now_add=True)
    disc = models.BooleanField(default=False, verbose_name='Add In Disclaimer')
    hit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def post_count(self):
        return self.posts.all().count()    

    class Meta:
        #enforcing that there can not be two categories under a parent with same slug
        
        # __str__ method elaborated later in post.  use __unicode__ in place of

        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"     

    def __str__(self):                           
        full_path = [self.title]                  
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])    

class subcat(models.Model):
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcat', blank = True, null=True, help_text='Select Only Sub Category')
    title = models.CharField(max_length=100) 
    slug = AutoSlugField(populate_from='title', unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    disc = models.BooleanField(default=False, verbose_name='Add In Disclaimer')

    def __str__(self):
        return self.title

    class Meta:
        #enforcing that there can not be two categories under a parent with same slug
        
        # __str__ method elaborated later in post.  use __unicode__ in place of

        unique_together = ('slug', 'parent',)
        #This is for outside or main which shows outside panel.    
        verbose_name_plural = "Sub Categories"     

    def __str__(self):                           
        full_path = [self.title]                  
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])    

class MainCourse(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True, null=False, editable=True)
    disc = models.BooleanField(default=False, verbose_name='Add In Disclaimer')

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=500)
    meta_tags = models.CharField(max_length=2000, blank=True)
    meta_desc = models.TextField(max_length=2000, blank=True)
    slug = AutoSlugField(populate_from='title', max_length=500, unique=True, null=False)
    image = models.ImageField(upload_to='media/post')
    image_alt_name = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='media/post') #If user want to add university logo(Slider and Post) 
    desc = RichTextField(blank=True, null=True)
    #for live classes or offline classes
    badge = models.CharField(max_length=70)
    youtube = models.URLField(max_length=500, default='' )
    author = models.CharField(max_length=20, default="admin" )
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name="posts")
    subcategory = models.ForeignKey(subcat, on_delete=models.CASCADE, default=1, related_name="subcat", blank=True, null=True)
    hit = models.PositiveIntegerField(default=0) #This field is for popular posts
    button_text = models.CharField(max_length=20, default="Apply Now") #Apply Now and enroll button text
    slider_post = models.BooleanField(default=False, blank=True)
    maincourse = models.ManyToManyField(MainCourse, blank=True, related_name='posts')
    price = models.IntegerField(default=0)
    old_price = models.IntegerField(default=0)
    discount = models.IntegerField()
    emi_start_price = models.IntegerField()
    why_title = models.CharField(max_length=500, blank=True)
    why1 = RichTextField(blank=True)
    why2 = RichTextField(blank=True)
    why3 = RichTextField(blank=True)
    file = models.FileField(upload_to='media/certificate', null=True, blank=True)
    disc = models.BooleanField(default=False, verbose_name='Add In Disclaimer')
    drive_link = models.URLField(max_length=500, blank=True, null=True, default='')  # Add Google Drive link
    
    def __str__(self):
        return self.title    
        
    def get_rating(self):
        total = sum(int(review['stars']) for review in self.review.values() )

        return total / self.reviews.count()

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='purchases')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Store the amount in a decimal field for accurate pricing
    purchase_date = models.DateTimeField(auto_now_add=True)  # Automatically set the date and time when the purchase is made

    def __str__(self):
        return f"{self.user.username} purchased {self.post.title} on {self.purchase_date}"

    class Meta:
        ordering = ['-purchase_date']  # Optional: Order by the latest purchase first


class Curriculam(models.Model):    
    title = models.CharField(max_length=500)
    Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='acc_posts')
    content = RichTextField(blank=True, null=True)

#Terms and Condition for blogs


class faq(models.Model):    
    title = models.CharField(max_length=500)
    Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='faq_posts')
    content = RichTextField(blank=True, null=True)




class features(models.Model):    
    title = models.CharField(max_length=500)
    Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='feature_posts')
    content = RichTextField(blank=True, null=True)

class boxes_three(models.Model):
    title = models.CharField(max_length=70)
    slug = AutoSlugField(populate_from='title', unique=True, null=False, editable=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title    

  



  



class clients(models.Model):    
    image= models.ImageField(upload_to='media/clients',null=True,blank=True)




    



class ChatMessage(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user_message}, Bot: {self.bot_response}"