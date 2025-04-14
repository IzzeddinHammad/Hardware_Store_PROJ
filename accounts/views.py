from django.contrib.auth import views as auth_views
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from .models import Profile, CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from .models import Profile, CustomUser
from .forms import CustomUserCreationForm



class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Add user to appropriate group based on the 'is_vendor' field
        if form.cleaned_data.get('is_vendor'):
            vendor_group, created = Group.objects.get_or_create(name='Vendor')
            self.object.groups.add(vendor_group)
        else:
            customer_group, created = Group.objects.get_or_create(name='Customer')
            self.object.groups.add(customer_group)

        # Save the date of birth to the user's profile
        date_of_birth = form.cleaned_data.get('date_of_birth')
        Profile.objects.create(user=self.object, date_of_birth=date_of_birth)

        return response




class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'registration/edit_profile.html'
    fields = ['date_of_birth']

class ProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'
    context_object_name = 'profile'

class ProfileCreateView(CreateView):
    model = Profile
    template_name = 'registration/create_profile.html'
    fields = ['date_of_birth']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)