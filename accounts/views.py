from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView , DetailView , CreateView
from .models import Profile , CustomUser
from .forms import CustomUserCreationForm
# Create your views here.


class SignUpView(generic.CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    # def form_valid(self, form):
    #     # Save the new user
    #     response = super().form_valid(form)
    #     # Add user to the Customer group
    #     customer_group, created = Group.objects.get_or_create(name='Customer')
    #     self.object.groups.add(customer_group)
    #     return response # Redirect to success URL



class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'registration/edit_profile.html'
    fields = ['date_of_birth']  # Add any other fields you want to edit


class ProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'
    context_object_name = 'profile'  # This makes the profile accessible in the template


class ProfileCreateView(CreateView):
    model = Profile
    template_name = 'registration/create_profile.html'
    fields = ['date_of_birth']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)