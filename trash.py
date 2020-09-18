from accounts.models import *
user1 = User.objects.get(username="jo")
cus1 = Customer.objects.get(user=user1)
CustomerProfile.objects.create(user=cus1)
restaurant = Restaurant.objects.get(company_name="mcdonald")
men1 = Menu.objects.get(restaurant=restaurant)
orders = men1.order_set.all()

###################### STILL CHANGING USER ##########################


def register(request):
    regsiter_form = RegistrationForm()
    if request.method == 'POST':
        form = regsiter_form(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(username=request.POST['username'],
                                                email=request.POST['email'],
                                                password=request.POST['password1'])
            new_user.is_active = False
            new_user.save()
            return HttpResponseRedirect(reverse('index'))
    return render_to_response('registration/registration_form.html'{'form': regsiter_form})
