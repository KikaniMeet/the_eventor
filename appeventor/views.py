from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from appeventor.models import datadesire ,adminuser,user_query,reservation
from django.conf import settings
from django.http import JsonResponse
from .forms import FakePaymentForm,FeedbackForm
from .models import FakePayment,Feedback,UserDocument

# Create your views here.
def home(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']  
        user = datadesire.objects.get(id=user_id)
        return render(request,"index.html",{'user':user})
    return render(request,"index.html")

def about(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']  
        user = datadesire.objects.get(id=user_id)
        return render(request,"about.html",{'user':user})
    return render(request,"about.html")

def rent_venue(request):
    if request.method == "POST":
         name=request.POST.get("name")
         email=request.POST.get("email")
         phone=request.POST.get("phone-number")
         company=request.POST.get("company-organization")
         venue=request.POST.get("venue-requested")
         event=request.POST.get("type-event")
         date1=request.POST.get("date-requested-first")
         date2=request.POST.get("date-requested-second")
         about=request.POST.get("about-event-hosting")
         data=reservation.objects.create(name=name,email=email,phone=phone,company=company,venue=venue,event=event,date1=date1,date2=date2,about=about)
         data.save()
    if 'user_id' in request.session:
        user_id = request.session['user_id']  
        user = datadesire.objects.get(id=user_id)
        return render(request,"rent-venue.html",{'user':user})
    return render(request,"rent-venue.html")

def shows_events(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']  
        user = datadesire.objects.get(id=user_id)
        return render(request,"shows-events.html",{'user':user})
    return render(request,"shows-events.html")

def corporate_party(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']  
        user = datadesire.objects.get(id=user_id)
        return render(request,"corporate_party.html",{'user':user})
    return render(request,"corporate_party.html")

def tickets(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']  
        user = datadesire.objects.get(id=user_id)
        return render(request,"tickets.html",{'user':user})
    return render(request,"tickets.html")

def ticket_details(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']  
        user = datadesire.objects.get(id=user_id)
        amount=request.GET.get("amount","0")
        event=request.GET.get("event",'None')
        return render(request,"ticket-details.html",{'user':user,'amount':amount,'event':event})
    return render(request,"ticket-details.html")

def event_details(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']  
        user = datadesire.objects.get(id=user_id)
        return render(request,"event-details.html",{'user':user})
    return render(request,"event-details.html")

def forgot_password(request):
    if request.method == "POST":
        
        email = request.POST['email']
        user = datadesire.objects.filter(email=email).first()
        if user:
            # Redirect to reset page with user id
            return redirect('reset-password', user_id=user.id)
        else:
            return render(request, 'forgot_password.html', {'error': 'Email not found'})
    return render(request, 'forgot_password.html')

def reset_password(request, user_id):
    user = get_object_or_404(datadesire, id=user_id)
    
    if request.method == "POST":
        new_password = request.POST['password']
        user.password = new_password
        user.save()
        return redirect('login_user')

    return render(request, 'reset_password.html', {'user': user})

def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # Check if email exists in database
        user = datadesire.objects.filter(email=email, password=password).first()

        if user:
            request.session['user_id'] = user.id  # Session 
            return redirect(home)  # Redirect to dashboard page
        else:
            error = "Invalid email or password"
            return render(request, "login.html", {'error': error})

    return render(request, "login.html")

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("id"):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def user_register(request):
    if request.method == "POST":
        name = request.POST['username']
        email = request.POST['email']
        phone=request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if email already exists
        if datadesire.objects.filter(email=email,phone=phone).exists():
            error = "This email is already registered. Please use a different email."
            return render(request, "register.html", {'error': error})

        # Check password match
        if password1 != password2:
            error = "Passwords do not match."
            return render(request, "register.html", {'error1': error})
        # If email is unique and passwords match, create a new user
        user = datadesire.objects.create(name=name, email=email, password=password1)
        user.save()

        return redirect(user_login)  # Ensure 'user_login' is a valid view name

    return render(request, "register.html")

def user_logout(request):
    request.session.flush()
    return redirect(user_login)

#admin side

def pages_login(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        try:
            user = adminuser.objects.filter(username=username, password=password).first()
            if user:
        # Set session data
                request.session['id'] = user.id
                request.session['username'] = user.username 
                return redirect(adminhome)
            else:
                 HttpResponse("Invalid credentials.")
        except Exception as e:
            return HttpResponse(f"Error: {e}")
        
    return render(request,"admin/pages-login.html")
# def add_admin(request):
    # name="darshil"
    # username="darshil@gmail.com"
    # password="darshil@123"
    # data=adminuser.objects.create(name=name,username=username,password=password)
    # data.save()

def adminhome(request):
    data=request.session.get('id')
    user=adminuser.objects.get(id=data)
    return render(request,"admin/index2.html",{'user':user})

def client_profile(request):
    data=request.session.get('id')
    user=adminuser.objects.get(id=data)
    data=datadesire.objects.all()
    return render(request,"admin/client-profile.html",{'user':user,'show':data})


def send_suggestions(request):
    data=request.session.get('id')
    user1=adminuser.objects.get(pk=data)
    user=adminuser.objects.get(id=data)
    # adminuser.objects.filter(is_read=False).update(is_read=True)
    if request.method == "POST":
        suggestion=request.POST.get("suggestion")
        # adminuser.objects.filter(is_read=False).update(is_read=True)
        user1.suggestion=suggestion
        user1.save()      
    return render(request,"admin/send-suggestions.html",{'user':user})

def admin_profile(request):
    data=request.session.get('id')
    user=adminuser.objects.get(id=data)
    return render(request,"admin/users-profile.html",{'user':user})

def view_documents(request):
    data=request.session.get('id')
    user=adminuser.objects.get(id=data)
    return render(request,"admin/view-documents.html",{'user':user})

def view_receive_payment(request):
    data=request.session.get('id')
    user=adminuser.objects.get(id=data)
    amount=FakePayment.objects.all()
    return render(request,"admin/view-receive-payment.html",{'user':user,"amount_show":amount})
def view_reservation(request):
    data=request.session.get('id')
    user=adminuser.objects.get(id=data)
    amount=reservation.objects.all()
    return render(request,"admin/reservation.html",{'user':user,"reservaton_detail":amount})

def view_suggestions(request):
    adminuser.objects.filter(is_read=False).update(is_read=True)
    data=request.session.get('id')
    user=adminuser.objects.get(id=data)
    query=user_query.objects.all()
    print(query)
    return render(request,"admin/view-suggestions.html",{'user':user,'data':query})

def admin_log_out(request):
    request.session.flush()  
    return redirect(pages_login)

def delete(request,id):
    data=datadesire.objects.get(pk=id)
    data.delete()
    return redirect(client_profile)
def update(request,id):
    return redirect(client_profile)


#client side


def log_out(request):
    request.session.flush()  
    return redirect(user_login)


# client profile panal

def clienthome(request):
    data=request.session.get('user_id')
    user=datadesire.objects.get(id=data)
    print(user)
    return render(request,"clientpenal/index.html",{'user':user})

def payment_info(request):
    data=request.session.get('user_id')
    user=datadesire.objects.get(id=data)
    user=user.email
    amount=FakePayment.objects.filter(email=user)
    # print(amount)
    return render(request,"clientpenal/payment-info.html",{'user':user,'amount_detail':amount})

def Reservation_view(request):
    data=request.session.get('user_id')
    user=datadesire.objects.get(id=data)
    reservation_data=reservation.objects.all()
    # print(amount)
    return render(request,"clientpenal/reservation.html",{'user':user,'reservaton_detail':reservation_data})

def profile(request):
    data=request.session.get('user_id')
    user=datadesire.objects.get(id=data)
    return render(request,"clientpenal/profile.html",{'user':user})

def document(request):
    data=request.session.get('user_id')
    user=datadesire.objects.get(id=data)
    if request.method == "POST":
        document_type = request.POST.get("d_id")
        document_file = request.FILES.get("document")
        try:
            user_profile = datadesire.objects.get(id=user)  
        except datadesire.DoesNotExist:
            return redirect("login")  

        
        UserDocument.objects.create(user=user_profile, document_type=document_type, document_file=document_file)
        return redirect(home) 
    return render(request,"clientpenal/send-document.html",{'user':user})
def view_suggestion(request):
    data=request.session.get('user_id')
    user=datadesire.objects.get(id=data)
    data=adminuser.objects.all()
    return render(request,"clientpenal/view_suggestion.html",{'user':user,'data':data})

def send_query(request):
    data=request.session.get('user_id')
    user=datadesire.objects.get(id=data)
    if request.method == "POST":
        email=request.POST.get("email")
        query=request.POST.get("query")
        user=user_query.objects.create(Q_email=email,query=query)
        user.save()
        return redirect(send_query)
    return render(request,"clientpenal/send-query.html",{'user':user})

def user_edit(request,id):
    data=datadesire.objects.get(pk=id)
    if request.method == "POST":
        data.name=request.POST.get("name")
        data.phone=request.POST.get("number")
        data.email=request.POST.get("email")
        data.password=request.POST.get("password")
        data.save()
        return redirect(profile)
    return render(request,"clientpenal/profile1.html",{'data':data})



def fake_payment_view(request):
    if request.session.get("user_id"):
        user_id = request.session['user_id']  
        user = datadesire.objects.get(id=user_id)
        amount = request.GET.get("amount", 210)
        if request.method == "POST":
            form = FakePaymentForm(request.POST)
            if form.is_valid():
                payment = form.save()
                return redirect(payment_success,transaction_id=payment.transaction_id)
        else:
            form = FakePaymentForm()
        return render(request, 'payment_form.html', {'form': form,"amount":amount,"user":user})
    return redirect(home)

def payment_success(request, transaction_id):
    payment = FakePayment.objects.get(transaction_id=transaction_id)
    return render(request, 'payment_success.html', {'payment': payment})

def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback_success')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

def feedback_success(request):
    return render(request, 'feedback_success.html')

def get_notification_count(request):
    count = adminuser.objects.filter(is_read=False).count()
    return JsonResponse({'count': count})