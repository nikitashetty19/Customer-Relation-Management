from django.shortcuts import render,redirect
from .models import *
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthorised_user,allowed_users,admin_only
from django.contrib.auth.models import Group



from .forms import OrderForm,CreatUserForm,CustomerForm

from .filters import OrderFilter
from django.contrib import messages

from django.forms import inlineformset_factory
# Create your views here.
@unauthorised_user
def registerPage(request):
    form=CreatUserForm()
    if request.method=="POST":
        form=CreatUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')

            group=Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user)
            messages.success(request,'Account was created for ' + username)
            return redirect('login')
    context={'form':form}    
    return render(request,'accounts/register.html',context)

@unauthorised_user
def loginPage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username ,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password provided is incorrect')
    context={}
    return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()
    total_orders=orders.count()
    delivered=orders.filter(status="Delivered").count()
    pending=orders.filter(status="Pending").count()

    context={'orders':orders,'cust':customers,
             'total_orders':total_orders,'delivered':delivered,
             'pending':pending}
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders=request.user.customer.order_set.all()
    total_orders=orders.count()
    delivered=orders.filter(status="Delivered").count()
    pending=orders.filter(status="Pending").count()

    print("ORDERS: ",orders)
    context={'orders':orders,'total_orders':total_orders,'delivered':delivered,
             'pending':pending}
    return render(request,'accounts/user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    if request.method=="POST":
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()


    context={'form':form}
    return render(request,'accounts/accountsettings.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    products= Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    total_orders=orders.count()
    myFilter=OrderFilter(request.GET,orders)
    orders=myFilter.qs

    context={'customer':customer,'orders':orders,'total_orders':total_orders,'myFilter':myFilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    customer=Customer.objects.get(id=pk)
    # form=OrderForm(initial={'customer':customer})
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method=='POST':
        # print('Printing Post:',request.POST)
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={'formset':formset}
    
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)
    if request.method=='POST':
        # print('Printing Post:',request.POST)
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/') 
    context={'form':form}
    
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    context={'item':order}
    if request.method=='POST':
        order.delete()
        return redirect('/')
    return render(request,'accounts/delete.html',context)

