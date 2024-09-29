from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.home, name='home'),

    #Custom admin panel urlss
    path('webadmin/', views.webadmin, name='webadmin'),
    path('addpost/', views.add_post, name='addpost'),
    path('addcat/', views.add_cat, name='addcat'),
    path('webadmin/addleftcat/', views.add_leftcat, name='addleftcat'),
    path('webadmin/addmiddlecat/', views.add_middlecat, name='addmiddlecat'),
    path('webadmin/addrightcat/', views.add_rightcat, name='addrightcat'),
    path('add_course/', views.add_course, name='addcourse'),
    path('allposts/', views.allposts, name='allposts'),
    path('allcat/', views.allcat, name='allcat'),
    path('allusers/', views.allusers, name='allusers'),
    path('allcourse/', views.allcourse, name='allcourses'),
    path('orders/', views.orders_view, name='orders'),
    # path('orderdetail/<int:id>', views.order_details, name='orderdetail'),
    path('webadmin/editpost/<int:id>', views.edit_post, name='editpost'),
    path('webadmin/deletepost/<int:id>', views.delete_post, name='deletepost'),
    path('webadmin/editcat/<int:id>', views.edit_cat, name='editcat'),
    path('webadmin/deletecat/<int:id>', views.delete_cat, name='deletecat'),
    path('webadmin/editcourse/<int:id>', views.edit_course, name='editcourse'),
    path('webadmin/deletecourse/<int:id>', views.delete_course, name='deletecourse'),
    path('webadmin/add_faq/', views.add_faq, name='add_faq'),
    path('webadmin/edit_faq/<int:id>', views.edit_faq, name='edit_faq'),
    path('webadmin/delete_faq/<int:id>', views.delete_faq, name='delete_faq'),
    path('webadmin/allfaq/', views.allfaq, name='allfaq'),
    path('webadmin/add_features/', views.add_features, name='add_features'),
    path('webadmin/edit_features/<int:id>', views.edit_features, name='edit_features'),
    path('webadmin/delete_features/<int:id>', views.delete_features, name='delete_features'),
    path('webadmin/allfeatures/', views.allfeatures, name='allfeatures'),
    path('webadmin/add_curriculam/', views.add_curriculam, name='add_curriculam'),
    path('webadmin/edit_curriculam/<int:id>', views.edit_curriculam, name='edit_curriculam'),
    path('webadmin/delete_curriculam/<int:id>', views.delete_curriculam, name='delete_curriculam'),
    path('webadmin/allcurriculam/', views.allcurriculam, name='allcurriculam'),
    path('webadmin/add_subcatg/', views.add_subcatg, name='add_subcatg'),
    path('webadmin/edit_subcatg/<int:id>', views.edit_subcatg, name='edit_subcatg'),
    path('webadmin/delete_subcatg/<int:id>', views.delete_subcatg, name='delete_subcatg'),
    path('webadmin/allsubcatg/', views.allsubcatg, name='allsubcatg'),

    #User panel urls
    path('chatbot/',views.chatbot, name='chatbot'),
    path('userlogin/', views.login, name='userlogin'),
    path('usersignup/', views.signup, name='usersignup'),
    path('userlogout/', views.logout, name='logout'),
    path('userdashboard/', views.userdashboard, name='userhome'),
    path('userprofile/', views.userprofile, name='profile'),
    path('userdetail/<int:id>', views.userdetails, name='userdetails'),
    path('edituserprofile/', views.edit_profile, name='editprofile'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('user_orders/', views.user_orders, name='user_orders'),

    #Public urls

    path('search/', views.search, name='search'),



    path('filter/<str:catslug>', views.post_by_category, name='catpost'),
    path('subcat/<str:subcatslug>', views.subcat_by_category, name='subcat'),
    path('<str:postslug>', views.allpost_by_category, name='allcatpost'),
    path('<str:category_slug>/<str:slug>', views.post_details, name='details'),
    
    # Enroll now URL
    path('<str:category_slug>/<str:slug>/enroll/', views.enroll_now, name='enroll_now'),

    # Payment page URL
    path('<str:category_slug>/<str:slug>/enroll/payment/', views.payment_page, name='payment_page'),

    # Payment success URL
    path('payment/success/', views.payment_success, name='payment_success'),
    path('purchases/', views.purchase_history, name='purchase_history'),
    path('courses/', views.courses, name='courses'),            
    path('allcourses/', views.totalposts, name='all-courses'), 



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
