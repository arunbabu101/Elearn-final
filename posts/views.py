from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as loginUser, update_session_auth_hash
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.urls import reverse
import json
from time import time
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from edureka.settings import *
import razorpay
KEY_ID = settings.RAZORPAY_KEY_ID
KEY_SECRET = settings.RAZORPAY_KEY_SECRET
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
from django.contrib.auth import authenticate, login as auth_login

 
# Create your views here.

def home(request):
    allposts = Post.objects.all().filter(maincourse=True)
    totalposts = Post.objects.all().order_by('-date')[:8]
    slider_post = Post.objects.all().filter(slider_post=True)
    top_three_catg = Category.objects.filter(top_three_cat=True)[:3]
    main_course = MainCourse.objects.all()
    allcat = Category.objects.all()
    categories = Category.objects.all().filter(top_three_cat=False).filter(more=False).order_by('-created_at')[:7]
    footcategories = Category.objects.filter(parent=None)[:2]
    catg = Category.objects.all().exclude(parent=None).order_by('-created_at')[:7]
    # catg_parent = Category.objects.all().exclude(parent=True).order_by('-hit')
    latest_catg = Category.objects.filter(parent=None)[:5]
    latest_catg_all = Category.objects.filter(parent=None)[5:]
    latest_post = Post.objects.order_by('-date')[:4]
    context = {'allposts':allposts, 'main_course':main_course, 'top_three_catg':top_three_catg, 'catg':catg, 'slider_post':slider_post, 'latest_catg':latest_catg, 'latest_post':latest_post, 'totalposts':totalposts, 
    
    # 'catg_parent':catg_parent,
     'allcat':allcat, 'categories':categories, 'footcategories':footcategories, 'latest_catg_all':latest_catg_all}
    return render(request, 'core/index.html', context)

def totalposts(request):
    total = Post.objects.all()
    context = {'total':total}
    return render(request, 'core/total.html', context)

def post_by_category(request, catslug):
    posts = Post.objects.all()
    cat_post = Post.objects.filter(category__slug=catslug)
    allposts = Post.objects.all().filter(maincourse=True)
    slider_post = Post.objects.all().filter(slider_post=True)
    top_three_catg = Category.objects.filter(top_three_cat=True)[:3]
    main_course = MainCourse.objects.all()
    allcat = Category.objects.all()
    categories = Category.objects.filter(parent=None).order_by('-created_at')[:7]
    footcategories = Category.objects.filter(parent=None)[:2]
    catg = Category.objects.all().exclude(parent=None).order_by('-created_at')[:7]
    catg_parent = Category.objects.all().exclude(parent=True)
    latest_catg = Category.objects.filter(parent=None)[:5]
    latest_post = Post.objects.order_by('-date')[:4]
    latest_catg_all = Category.objects.filter(parent=None)[5:]
    context = {'latest_catg_all':latest_catg_all,  'posts':posts, 'cat_post':cat_post,'allposts':allposts, 'main_course':main_course, 'top_three_catg':top_three_catg, 'catg':catg, 'slider_post':slider_post, 'latest_catg':latest_catg, 'latest_post':latest_post}
    return render(request, 'core/index.html', context)

def allpost_by_category(request, postslug):
    posts = Post.objects.all()
    cat_post = Post.objects.filter(category__slug=postslug)
    subcat_post = Post.objects.filter(subcategory__slug=postslug)
    allposts = Post.objects.all().filter(maincourse=True)
    allcat = Category.objects.all()
    context = {'posts':posts,'subcat_post':subcat_post, 'cat_post':cat_post,'allposts':allposts,'allcat':allcat,}
    return render(request, 'core/allposts.html', context)

def subcat_by_category(request, subcatslug):
    allcats = get_object_or_404(Category, slug=subcatslug)
    category = subcat.objects.filter(slug=subcatslug)
    # allsubcatg = allcats.subcat.filter(parent__slug=slug)
    cat_subcat = subcat.objects.filter(parent__slug=subcatslug)
    context = {'cat_subcat':cat_subcat, 'category':category, 'allcats':allcats}
    return render(request, 'core/catg_subcat.html', context)
  
import re

def convert_to_embed_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    match = re.match(youtube_regex, url)
    if match:
        video_id = match.group(6)
        embed_url = f"https://www.youtube.com/embed/{video_id}"
        return embed_url
    return url  # Return the original URL if it doesn't match the pattern

def convert_to_embed_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    match = re.match(youtube_regex, url)
    if match:
        video_id = match.group(6)
        embed_url = f"https://www.youtube.com/embed/{video_id}"
        return embed_url
    return url  # Return the original URL if it doesn't match the pattern

def post_details(request, category_slug, slug):
    posts = Post.objects.filter(slug=slug).first()
    category = Post.objects.filter(slug=category_slug)
    catg_parent = Category.objects.all().exclude(parent=True)
    allcat = Category.objects.all()
    allpost = get_object_or_404(Post, slug=slug)
    
    # For add curriculam
    curriculam = Curriculam.objects.filter(Post=allpost)
    
    # For class features
    feature = features.objects.filter(Post=allpost)
    
    # For frequently asked questions
    faqs = faq.objects.filter(Post=allpost)
    
    # For Timing
    
    # Convert YouTube URL to embed URL
    youtube_url = convert_to_embed_url(allpost.youtube) if allpost.youtube else None
    
    # For Reviews
    if request.method == 'POST' and request.user.is_authenticated:
        allstars = request.POST.get('stars', 3)
        allcontent = request.POST.get('content', '')
        return redirect('home')
    
    context = {
        'posts': posts,
        'category': category,
        'allcat': allcat,
        'catg_parent': catg_parent,
        'curriculam': curriculam,
        'allpost': allpost,
        'features': feature,
        'faqs': faqs,
        'time': time,
        'youtube_url': youtube_url
    }
    return render(request, 'core/details.html', context)


def enroll_now(request, category_slug, slug):
    posts = Post.objects.filter(slug=slug).first()
    category = Post.objects.filter(slug=category_slug)
    # Check if the user is logged in
    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'core/payment_page.html', context)
    
@login_required
def payment_page(request, category_slug, slug):
    post = get_object_or_404(Post, category__slug=category_slug, slug=slug)

    if request.method == 'POST':
        # Handle payment details submission
        name = request.POST.get('name')
        payment_method = request.POST.get('payment_method')  # UPI, card, etc.
        
        # Payment processing logic here
        # For demo purposes, just create a purchase record
        Purchase.objects.create(user=request.user, post=post, amount=post.price)

        # After payment, redirect to success page
        return redirect('payment_success')

    context = {
        'posts': post,
        'category_slug': category_slug,
    }
    return render(request, 'core/payment_success.html', context)
    

def payment_success(request):
    return render(request, 'core/payment_success.html')

@login_required
def purchase_history(request):
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'users/purchase_history.html', {'purchases': purchases})

def search(request):
    search = request.GET['search']
    totalposts = Post.objects.filter(title__icontains=search)
    # allpostcontent = Post.objects.filter(desc__icontains=search)
    context = {'totalposts':totalposts, 'search':search}
    return render(request, 'core/search.html', context)





def courses(request):
    main_course = MainCourse.objects.all()
    context = {'main_course':main_course}
    return render(request, 'core/courses.html', context)





   

# UserSignup Form
def signup(request):
    next_page = request.GET.get('next')
    form = CustomerCreationForm()
    customerForm = CustomerForm()
    
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        customerForm = CustomerForm(request.POST, request.FILES)
        if form.is_valid() and customerForm.is_valid():
            user = form.save()
            user.email = user.username
            user.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('userlogin')
    
    context = {'form': form, 'customerForm': customerForm}
    return render(request, 'users/signup.html', context)

# UserSignup Form
def login(request):
    if request.method == 'GET':
        next_page = request.GET.get('next')
        context = {'next': next_page}
        return render(request, 'users/login.html', context)
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            next_page = request.POST.get('next', 'home')
            return redirect(next_page)
        else:
            context = {'error': 'Invalid username or password', 'next': request.POST.get('next')}
            return render(request, 'users/login.html', context)

def logout(request):
    request.session.clear()
    return redirect('home')

def userdashboard(request):
    customer = Customer.objects.all()
    # if orders.exists() and carts.exists():
    #     order = orders[0]
    #     return render(request, 'users/index.html', context={'carts':carts,'orders':orders})
    context = {'customer':customer}
    return render(request, 'users/index.html', context)

def userprofile(request):
    customer = Customer.objects.get(user_id=request.user.id)
    context = {'customer':customer}
    return render(request, 'users/profile.html', context)

def user_orders(request):
    if request.user.is_authenticated:
        orders = Purchase.objects.filter(user=request.user).select_related('post')  # Get orders for the logged-in user
    else:
        orders = []
    return render(request, 'users/orders.html', {'orders': orders})

def edit_profile(request):
    if request.method == 'POST':
        user_form = CustomerCreationEditForm(request.POST or None, request.FILES or None, instance=request.user)
        profile_form = CustomerEditForm(request.POST or None, request.FILES or None, instance=request.user.customer)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            # print(user_form)
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = CustomerCreationEditForm(instance=request.user)
        profile_form = CustomerEditForm(instance=request.user.customer)
    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('userhome')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/edit_password.html', {
        'form': form
    })





#----------------------------------------------------------------------



from datetime import datetime, timedelta
from django.db.models import Count

from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.models import User
from .models import Category, Post, Purchase, MainCourse
from django.utils import timezone
from datetime import timedelta

def webadmin(request):
    # Common Insights
    user_count = User.objects.count()
    course_count = Post.objects.count()
    category_count = Category.objects.count()
    purchase_count = Purchase.objects.count()

    # Posts by Category
    categories = Category.objects.annotate(post_count=Count('posts'))
    category_names = [category.title for category in categories]
    category_post_counts = [category.post_count for category in categories]

    # User Registrations Over Time
    today = timezone.now()
    last_30_days = today - timedelta(days=30)
    user_registrations = User.objects.filter(date_joined__gte=last_30_days).extra({'date': "date(date_joined)"}).values('date').annotate(count=Count('id')).order_by('date')
    registration_dates = [reg['date'].strftime('%Y-%m-%d') for reg in user_registrations]
    registration_counts = [reg['count'] for reg in user_registrations]

    # Course Distribution by Main Course
    main_courses = MainCourse.objects.annotate(course_count=Count('posts'))
    main_course_names = [course.title for course in main_courses]
    main_course_counts = [course.course_count for course in main_courses]

    # Purchase Distribution by Category
    category_purchases = Category.objects.annotate(purchase_count=Count('posts__purchases'))
    category_purchase_counts = [category.purchase_count for category in category_purchases]

    context = {
        'user_count': user_count,
        'course_count': course_count,
        'category_count': category_count,
        'purchase_count': purchase_count,
        'category_names': category_names,
        'category_post_counts': category_post_counts,
        'registration_dates': registration_dates,
        'registration_counts': registration_counts,
        'main_course_names': main_course_names,
        'main_course_counts': main_course_counts,
        'category_purchase_counts': category_purchase_counts,
    }

    return render(request, 'webadmin/index.html', context)






def add_post(request):
    posts = PostForm()
    if request.method == 'POST':
        posts = PostForm(request.POST, request.FILES)
        if posts.is_valid():
            posts.save()
            messages.success(request, "Post Added Successfully !!")
            return redirect('allposts')
    return render(request, "webadmin/addpost.html", {'post': posts})


def add_course(request):
    course= Maincourse()
    if request.method=='POST':
        course=Maincourse(request.POST, request.FILES)
        if course.is_valid():
            course.save()
        messages.success(request, "Course Added Sucessfully !!")    
        return redirect('allcourses')
    return render(request, "webadmin/addcourse.html", {'course':course})


def add_cat(request):
    category= CatForm()
    if request.method=='POST':
        category=CatForm(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addcat.html", {'category':category})

def add_curriculam(request):
    category= CatForm()
    if request.method=='POST':
        category=CatForm(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('webadmin')
    return render(request, "webadmin/addcat.html", {'category':category})

#This is for show all Posts in Custom Admin Panel
def allposts(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'webadmin/allposts.html', context)

#This is for show all Users in Custom Admin Panel
def allusers(request):
    # users = User.objects.all()
    customer = Customer.objects.all()
    context = {
        # 'users':users
    'customer':customer
    }
    return render(request, 'webadmin/allusers.html', context)

def userdetails(request, id):
    customer = Customer.objects.filter(id=id).first()
    context = {'customer':customer}
    return render(request, 'webadmin/user_detail.html', context)




def orders_view(request):
    orders = Purchase.objects.select_related('user', 'post').all()  # Adjust based on your model relationships
    return render(request, 'webadmin/orders.html', {'orders': orders})
    
#This is for show all Categories in Custom Admin Panel
def allcat(request):
    cat = Category.objects.filter(parent=None).order_by('hit')
    context = {'cat':cat}
    return render(request, 'webadmin/allcat.html', context)

def allcourse(request):
    course = MainCourse.objects.all()
    context = {'course':course}
    return render(request, 'webadmin/allcourse.html', context)

def edit_post(request, id):
    if request.method == 'POST':
        posts = Post.objects.get(id=id)
        editpostForm= EditPostForm(request.POST or None, request.FILES or None, instance=posts)
        if editpostForm.is_valid():
            editpostForm.save()
        messages.success(request, "Post Update Sucessfully !!")
        return redirect('allposts')
    else:
        posts = Post.objects.get(id=id)
        editpostForm= EditPostForm(instance=posts)

    return render(request, "webadmin/editposts.html", {'editpost':editpostForm})
    
def delete_post(request, id):
    delete = Post.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Post Deleted Successfully.")
    return redirect('allposts')


#For edit the categories
def edit_cat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        editcatForm= CatForm(request.POST or None, request.FILES or None, instance=cat)
        if editcatForm.is_valid():
            editcatForm.save()
            messages.success(request, "Category Update Sucessfully !!")
            return redirect('allcat')
        else:
            messages.warning(request, "Category is not Updated !!")
            return redirect('allcat')    
    else:
        cat = Category.objects.get(id=id)
        editcatForm= CatForm(instance=cat)

    return render(request, "webadmin/editcat.html", {'editcat':editcatForm})

#For delete the categories    
def delete_cat(request, id):
    delete = Category.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Category Deleted Successfully.")
    return redirect('allcat')


#For edit the course
def edit_course(request, id):
    if request.method == 'POST':
        course = MainCourse.objects.get(id=id)
        editcourse= EditMaincourse(request.POST or None, request.FILES or None, instance=course)
        if editcourse.is_valid():
            editcourse.save()
        messages.success(request, "Course Update Sucessfully !!")
        return redirect('allcat')
    else:
        cat = MainCourse.objects.get(id=id)
        editcourse= EditMaincourse(instance=cat)

    return render(request, "webadmin/editcourse.html", {'editcourse':editcourse})

#For delete the course
def delete_course(request, id):
    delete = MainCourse.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "MainCourse Deleted Successfully.")
    return redirect('allcourses')    



    








def allfaq(request):
    f = faq.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allfaq.html', context)

def add_faq(request):
    faq= faqForm()
    if request.method=='POST':
        faq= faqForm(request.POST, request.FILES)
        if faq.is_valid():
            faq.save()
        messages.success(request, "faq Added Sucessfully !!")    
        return redirect('allfaq')
    return render(request, "webadmin/add_faq.html", {'faq':faq})

def edit_faq(request, id):
    if request.method == 'POST':
        faqs = faq.objects.get(id=id)
        EditfaqForm= faqForm(request.POST, instance=faqs)
        if EditfaqForm.is_valid():
            EditfaqForm.save()
        messages.success(request, "FAQ Update Sucessfully !!")
        return redirect('allfaq')
    else:
        faqs = faq.objects.get(id=id)
        EditfaqForm= faqForm(instance=faqs)   

    return render(request, "webadmin/editfaq.html", {'faqForm':EditfaqForm})

def delete_faq(request, id):
    delete = faq.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "faq Deleted Successfully.")
    return redirect('allfaq') 





def allfeatures(request):
    f = features.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allfeatures.html', context)

def add_features(request):
    features= featuresform()
    if request.method=='POST':
        features= featuresform(request.POST, request.FILES)
        if features.is_valid():
            features.save()
        messages.success(request, "Timings Added Sucessfully !!")    
        return redirect('allfeatures')
    return render(request, "webadmin/add_features.html", {'features':features})

def edit_features(request, id):
    if request.method == 'POST':
        feat = features.objects.get(id=id)
        editfeatures = featuresform(request.POST, instance=feat)
        if editfeatures .is_valid():
            editfeatures .save()
        messages.success(request, "featuress Update Sucessfully !!")
        return redirect('allfeatures')
    else:
        feat = features.objects.get(id=id)
        editfeatures = featuresform(instance=feat)   

    return render(request, "webadmin/edit_features.html", {'features':editfeatures })

def delete_features(request, id):
    delete = features.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Features Deleted Successfully.")
    return redirect('allfeatures') 

def allcurriculam(request):
    f = Curriculam.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allcurriculam.html', context)

def add_curriculam(request):
    curr= Curriculamform()
    if request.method=='POST':
        curr= Curriculamform(request.POST, request.FILES)
        if curr.is_valid():
            curr.save()
        messages.success(request, "Curriculam Added Sucessfully !!")    
        return redirect('allcurriculam')
    return render(request, "webadmin/add_curr.html", {'curr':curr})

def edit_curriculam(request, id):
    if request.method == 'POST':
        curr = Curriculam.objects.get(id=id)
        editcurr = Curriculamform(request.POST, instance=curr)
        if editcurr.is_valid():
            editcurr.save()
        messages.success(request, "Curriculam Update Sucessfully !!")
        return redirect('allcurriculam')
    else:
        curr = Curriculam.objects.get(id=id)
        editcurr = Curriculamform(instance=curr)   

    return render(request, "webadmin/edit_curriculam.html", {'editcurr':editcurr })

def delete_curriculam(request, id):
    delete = Curriculam.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Curriculam Deleted Successfully.")
    return redirect('allcurriculam') 

def allsubcatg(request):
    f = subcat.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allsubcat.html', context)

def add_subcatg(request):
    sub= subcatg()
    if request.method=='POST':
        sub= subcatg(request.POST, request.FILES)
        if sub.is_valid():
            sub.save()
        messages.success(request, "Subcat Added Sucessfully !!")    
        return redirect('allsubcatg')
    return render(request, "webadmin/add_subcat.html", {'sub':sub})

def edit_subcatg(request, id):
    if request.method == 'POST':
        sub = subcat.objects.get(id=id)
        editsub = subcatg(request.POST, instance=sub)
        if editsub.is_valid():
            editsub.save()
        messages.success(request, "Subcat Update Sucessfully !!")
        return redirect('allsubcatg')
    else:
        sub = subcat.objects.get(id=id)
        editsub = subcatg(instance=sub)   

    return render(request, "webadmin/edit_subcat.html", {'subcat':editsub })

def delete_subcatg(request, id):
    delete = subcat.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Subcat Deleted Successfully.")
    return redirect('allsubcatg') 








   

def add_leftcat(request):
    category= leftmenu()
    if request.method=='POST':
        category=leftmenu(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addleftcat.html", {'category':category})

#For edit the categories
def edit_leftcat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        editcatForm= leftmenu(request.POST or None, request.FILES or None, instance=cat)
        if editcatForm.is_valid():
            editcatForm.save()
            messages.success(request, "Category Update Sucessfully !!")
            return redirect('allcat')
        else:
            messages.warning(request, "Category is not Updated !!")
            return redirect('allcat')    
    else:
        cat = Category.objects.get(id=id)
        editcatForm= leftmenu(instance=cat)

    return render(request, "webadmin/editleftcat.html", {'editcat':editcatForm})

def add_middlecat(request):
    category= middlemenu()
    if request.method=='POST':
        category=middlemenu(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addmiddlecat.html", {'category':category})

#For edit the categories
def edit_middlecat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        editcatForm= middlemenu(request.POST or None, request.FILES or None, instance=cat)
        if editcatForm.is_valid():
            editcatForm.save()
            messages.success(request, "Category Update Sucessfully !!")
            return redirect('allcat')
        else:
            messages.warning(request, "Category is not Updated !!")
            return redirect('allcat')    
    else:
        cat = Category.objects.get(id=id)
        editcatForm= middlemenu(instance=cat)

    return render(request, "webadmin/editmiddlecat.html", {'editcat':editcatForm})

def add_rightcat(request):
    category= rightmenu()
    if request.method=='POST':
        category=rightmenu(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addrightcat.html", {'category':category})

#For edit the categories
def edit_rightcat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        editcatForm= rightmenu(request.POST or None, request.FILES or None, instance=cat)
        if editcatForm.is_valid():
            editcatForm.save()
            messages.success(request, "Category Update Sucessfully !!")
            return redirect('allcat')
        else:
            messages.warning(request, "Category is not Updated !!")
            return redirect('allcat')    
    else:
        cat = Category.objects.get(id=id)
        editcatForm= rightmenu(instance=cat)

    return render(request, "webadmin/editrightcat.html", {'editcat':editcatForm})

  

  



 
    




import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse


# Initialize the Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Add this new view to your views.py file
def chatbot(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        
        # Generate a response using Gemini
        response = model.generate_content(user_input)
        
        return JsonResponse({'response': response.text})
    
    return render(request, 'core/chatbot.html')


