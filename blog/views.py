from decimal import Context
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import  Post, Contact, BlogComment, Profileinfoform, Reviews, Bloglikes, Userprofile, Add_Category
from .forms import Edit_blog, post_blog, Userprofileimageform, Userprofilebannerform
from django.conf import settings
from django.core.mail import message, send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.db.models.query_utils import Q
from django.template import loader
from django.contrib.auth.decorators import login_required 
import datetime
from django.urls import reverse
import urllib
import urllib3
import json






# Create your views here.


def landing(request):
    cat_list = Add_Category.objects.all()
    post=Post.objects.all()
    context = {"posts": post, "cat_list": cat_list}
    return render(request, 'landing.html', context)
    


# def all_filter_post(request):
#     present_post = Post.objects.all()
#     cat_list = Add_Category.objects.all()
#     context = {"posts": present_post, "cat_list": cat_list}

#     return render(request, "post.html", context)


def filter_post(request, slug_cat):
    present_post = Post.objects.all()
    cat_list = Add_Category.objects.all()
    my_cat = Add_Category.objects.get(slug_cat=slug_cat)
    my_cat_id = my_cat.cat_id
    filter_post = Post.objects.filter(category_id=my_cat_id)
    context = {"posts": present_post, "cat_list": cat_list, "posts": filter_post}
    return render(request, "post.html", context)




 
# def home(request):
#     post = Post.objects.all()
#     #post = Post.objects.filter(view_post_bool=True)
#     #date = datetime.datetime.now()
#     #print(date)
#     context = {"posts": post}
#     return render(request, 'home.html', context)

def signIn(request):
    if request.method=="POST":   
        username = request.POST['username']
        password = request.POST['pass1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"Hello {username}, Your are successfully logedIn...!")
            return redirect("landing")
        else:
            messages.warning(request, "Invalid username and password.")
            return redirect("landing")      
    return render(request, "landing.html")



def signUp(request):
    if request.method == "POST":
        user_name=request.POST['username']
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if pass1 == pass2:
            if User.objects.filter(username=user_name).exists():
                messages.warning(request, 'Username already taken')
                return redirect('/')
            elif User.objects.filter(email=email).exists():
                messages.warning(request, 'Email already taken')
                return redirect('/')
            else:
                user = User.objects.create_user(username=user_name,email=email,password=pass1)
                user.first_name=first_name
                user.last_name=last_name
                user.save()
                messages.success(request, "Your account has been successfully created for login click on login button...!")
                return redirect('/')

        elif len(user_name) < 2 or len(user_name) >=15:
            messages.error("Please follow the conditions of username.")
            return redirect('/')
        else:
            messages.warning(request, 'Password does not match.')
            return redirect('/')      
    else:
        return render(request, 'error_404.html')

    
 
def signOut(request):
    logout(request)
    messages.info(request, "You have successfully signed out.")
    return redirect('/')



def error_404(request,exception):
    return render(request, 'error_404.html')



def about(request):
    return render(request, 'about.html')


def blog(request):
    return render(request, 'blog.html')

def contactus(request):
    if request.method=='POST':
        name=request.POST['name']
        contactno=request.POST['contactno']
        emailid=request.POST['email']
        content=request.POST['content']
    
        if name=="":
            messages.warning(request, "Please fill your name.")
            return redirect("contactus")
        elif contactno=="":
            messages.warning(request,"Please fill the contact number.")
            return redirect("contactus")
        elif emailid=="":
            messages.warning(request,"Please fill the emailid.")
            return redirect("contactus")
        elif content=="":
            messages.warning(request, "Please write some message.")
            return redirect("contactus")
        else:
            contact = Contact(name=name, contact=contactno, email=emailid, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent, we will contact you soon.")
            return redirect('contactus')
    else:
        return render(request, "contactus.html")

 
def Post_blog(request):
    context = {}
    if request.method == "POST":
        form = post_blog(request.POST, request.FILES)
        if request.user.is_authenticated:
            if form.is_valid():
                title = form.cleaned_data.get("title")
                category = form.cleaned_data.get("category")
                bannerimage = form.cleaned_data.get("bannerimage")
                thumbnailimg = form.cleaned_data.get("thumbnailimg")
                content = form.cleaned_data.get("content")
                user_id = User.objects.get(id=request.user.id)

                post_obj = Post.objects.create(
                                    title = title,
                                    category=category,
                                    bannerimage = bannerimage,
                                    thumbnailimg = thumbnailimg,
                                    content = content,
                                    user_id=user_id       
                                    )
                post_obj.save()
                messages.success(request, "Your post has been successfully uploaded...!")
                return redirect(reverse('post_blog'))         
    else:
        form = post_blog()
    context['form']= form
    return render(request, "post_blog.html", context)
    

 
def Detail_view(request, slug):
    all_category_li=['sports', 'technology', 'educational']
    # for single_cat in (Add_Category.objects.all()):
    #     all_category_li.append(single_cat)
    #print(all_category_li)
    if slug in all_category_li:
        present_post = Post.objects.all()
        cat_list = Add_Category.objects.all()
        my_cat = Add_Category.objects.get(slug_cat=slug)
        my_cat_id = my_cat.cat_id
        filter_post = Post.objects.filter(category_id=my_cat_id)
        context = {"posts": present_post, "cat_list": cat_list, "posts": filter_post}
        return render(request, "post.html", context)
        #return HttpResponse(0)
    else:
        post = Post.objects.get(slug=slug)
        count=0
        post.view=1
        count=count+1
        if (count%111)==0:
            post.view = post.view+1
            post.save()
        else:
            post.view
            post.save()
        
        is_liked=False
        if post.likes.filter(id=request.user.id).exists(): 
            is_liked = True

        comments= BlogComment.objects.filter(post=post, post_bool=True)
        replies = BlogComment.objects.filter(post=post).exclude(parent=None)
        replyDict = {}
        for reply in replies:
            if reply.parent.sno not in replyDict.keys():
                replyDict[reply.parent.sno] = [reply]
            else:
                replyDict[reply.parent.sno].append(reply)
        
        context = {"post": post,
                # "userprofile": userprofile, 
                "comments": comments, 
                "user": request.user, 
                "replyDict": replyDict, 
                "is_liked": is_liked, 
                "total_likes": post.total_likes()
                }    
        return render(request, 'detail_view.html', context)



def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(id=postSno)
        parentSno = request.POST.get('parentSno')
        
        if parentSno=="":    
            comments=BlogComment(comment=comment, user=user, post=post)
            comments.save()
            messages.success(request, "Your comment is under review.")  
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comments=BlogComment(comment=comment, user=user, post=post, parent=parent)
            comments.save()
            messages.success(request, "Your reply has been posted successfully")  
    return redirect(f"/{post.slug}")


 
def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked=False
    if post.likes.filter(id=request.user.id).exists():  
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())


 
def Edit_bl(request, id):
    post = Post.objects.get(id=id)
    editblog = Edit_blog(instance=post)
    context = {'edit_blog': editblog}
    if request.method=='POST':
        form = Edit_blog(request.POST,request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,"Post has been successfully updated.")
            return redirect(reverse("edit_blog", args=[id]))
    else:
         form = Edit_blog()
    context['form']= form
    return render(request, 'edit_blog.html', context)


 
def Delete_blog(request,id):
    post = Post.objects.get(id=id)
    post.delete()
    messages.success(request, "Post has been deleted successfully...!")
    return redirect(reverse('landing'))
    

def search(request):
    search = request.GET['search']
    #searchtitle = Post.objects.get('title')
    if len(search) > 80:
        posts = []
    else:
        posts = Post.objects.filter(title__icontains=search)
    params = {'posts': posts, 'search': search}
    return render(request, 'search.html', params)


def userprofile(request):
    user = request.user
    userprofile = Userprofile.objects.filter(user_id=request.user.id)
    profileinfoform = Profileinfoform.objects.get(puser=request.user.id)
    user_posts=Post.objects.filter(user_id=request.user).order_by('-created_on')

    if request.method == 'POST':
        profileimg_form = Userprofileimageform(request.POST, request.FILES, instance=request.user.userprofile)
        bannerimg_form = Userprofilebannerform(request.POST, request.FILES, instance=request.user.userprofile)
        if profileimg_form.is_valid():
            profileimg_form = profileimg_form.save()
            bannerimg_form = bannerimg_form.save()
            messages.success(request,'Your Profile picture has been successfully updated!')
            return redirect('userprofile')
        else:
            print(profileimg_form.errors)
    else:
        profileimg_form = Userprofileimageform(instance=request.user.userprofile)
        bannerimg_form = Userprofilebannerform(instance=request.user.userprofile)
   
    context = {'user': user, 
               'user_posts': user_posts, 
               'profileinfoform': profileinfoform, 
               'userprofile': userprofile, 
               'profileimg_form': profileimg_form,
               'bannerimg_form': bannerimg_form,
               }
    template='userprofile.html'
    #print(user.userprofile.userprofileimg.url)
    #print(profileinfoform.lastname)
    return render(request,template,context)


 
def profileinfoform(request):
    context={}
    profileinfoform = Profileinfoform.objects.get(puser=request.user.id)
    user = User.objects.get(id=request.user.id)
    context["profileinfoform"]= profileinfoform

    if request.method == "POST":
        firstname = request.POST['firstname']
        middlename = request.POST['mname']
        lastname = request.POST['lname']
        phoneno1 = request.POST['pno']
        gender = request.POST['gender']
        address = request.POST['address']
        country = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']
        pincode = request.POST['pincode']
        dob = request.POST['dob']
        about = request.POST['about']
        university = request.POST['university']
        unistartdate = request.POST['startdate']
        unicompletiondate = request.POST['completiondate']
        unicity = request.POST['unicity']
        college = request.POST['college']
        collegestartdate = request.POST['collegestartdate']
        collegecompletiondate = request.POST['collegecompletiondate']
        collegecity = request.POST['collegecity']
        school = request.POST['school']
        schoolstartdate = request.POST['schoolstartdate']
        schoolcompletiondate = request.POST['schoolcompletiondate']
        schoolcity = request.POST['schoolcity']
        company = request.POST['company']
        experience = request.POST['experience']
        companycity = request.POST['companycity']
        skills = request.POST['skills']
        hobbies = request.POST['hobbies']
        abouthobbies = request.POST['abouthobbies']
        emailid = request.POST['emailid']
        phoneno2 = request.POST['contactno']
        permanentaddress = request.POST['address']
        website = request.POST['website']
        facebook = request.POST['facebook']
        twitter = request.POST['twitter']
        youtube = request.POST['youtube']
        linkedin = request.POST['linkedin']

        userinfo = Profileinfoform(
                                    name=firstname,
                                    middlename= middlename,
                                    lastname=lastname,
                                    phoneno1 = phoneno1,
                                    gender = gender,
                                    address = address,
                                    country = country,
                                    state = state,
                                    city = city,
                                    pincode=pincode,
                                    dob = dob,
                                    about = about,
                                    university = university,
                                    startdate = unistartdate,
                                    completiondate = unicompletiondate,
                                    unicity = unicity,
                                    college = college,
                                    collegestartdate = collegestartdate,
                                    collegecompletiondate = collegecompletiondate,
                                    collegecity = collegecity,
                                    school = school,
                                    schoolstartdate = schoolstartdate,
                                    schoolcompletiondate = schoolcompletiondate,
                                    schoolcity = schoolcity,
                                    company = company,
                                    experience = experience,
                                    companycity = companycity,
                                    technicalskills = skills,
                                    hobbies = hobbies,
                                    abouthobbies = abouthobbies,
                                    email = emailid,
                                    phoneno2 = phoneno2,
                                    permanentaddress = permanentaddress,
                                    website = website,
                                    facebook = facebook,
                                    twitter = twitter,
                                    youtube = youtube,
                                    linkedin = linkedin
                                    )
        userinfo.save()        

        user.first_name=firstname
        user.last_name=lastname
        user.email = emailid
        user.save()
        profileinfoform.middlename= middlename
        profileinfoform.phoneno1 = phoneno1
        profileinfoform.gender = gender
        profileinfoform.address = address
        profileinfoform.country = country
        profileinfoform.state = state
        profileinfoform.city = city
        profileinfoform.pincode=pincode
        profileinfoform.dob = dob
        profileinfoform.about = about
        profileinfoform.university = university
        profileinfoform.startdate = unistartdate
        profileinfoform.completiondate = unicompletiondate
        profileinfoform.unicity = unicity
        profileinfoform.college = college
        profileinfoform.collegestartdate = collegestartdate
        profileinfoform.collegecompletiondate = collegecompletiondate
        profileinfoform.collegecity = collegecity
        profileinfoform.school = school
        profileinfoform.schoolstartdate = schoolstartdate
        profileinfoform.schoolcompletiondate = schoolcompletiondate
        profileinfoform.schoolcity = schoolcity
        profileinfoform.company = company
        profileinfoform.experience = experience
        profileinfoform.companycity = companycity
        profileinfoform.technicalskills = skills
        profileinfoform.hobbies = hobbies
        profileinfoform.abouthobbies = abouthobbies
        profileinfoform.email = emailid
        profileinfoform.phoneno2 = phoneno2
        profileinfoform.permanentaddress = permanentaddress
        profileinfoform.website = website
        profileinfoform.facebook = facebook
        profileinfoform.twitter = twitter
        profileinfoform.youtube = youtube
        profileinfoform.linkedin = linkedin
        profileinfoform.save()
        
        messages.success(request, "Your profile has been successfully updated.")
        return redirect('userprofile') 
    return render(request, 'profileinfoform.html' , context)
    

def publicuserprofile(request, id):
    user = User.objects.get(id=id)
    profileinfoform = Profileinfoform.objects.get(puser=user.id)
    userprofile = Userprofile.objects.get(user_id=user.id)
   
    context={"user": user,
             "profileinfoform": profileinfoform,
             "userprofile": userprofile,
              }
    return render(request, 'publicuserprofile.html', context=context)

    




def review(request,id):
    if request.method=="post":
        user_name = request.user.user_name
        post = request.POST.get(id=id)
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        reviews=Reviews(user_name=user_name,post=post, review=review, rating=rating)
        reviews.save()
        messages.success(request,"Your review has been successfully submitted.")
        return redirect('detail_view/{{post.id}}/')
    return render(request, 'detail_view.html')



# Password reset start over here...!
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'localhost',
					"uid": urlsafe_base64_encode(force_bytes(user.id)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = loader.render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'shubhnesh0076@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
				return redirect("password_reset/done/")
            #messages.warning(request, "you entered wrong emailid.")
                
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})



    