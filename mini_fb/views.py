from django.views.generic import ListView, DetailView, CreateView
from .models import Profile
from django.urls import reverse
from .forms import *


class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'  # Correct template path
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Retrieve the 'pk' from URL parameters
        pk = self.kwargs['pk']
        # Get the corresponding Profile object
        profile = Profile.objects.get(pk=pk)
        # Add the Profile object to the context
        context['profile'] = profile
        return context

    def form_valid(self, form):
        # Retrieve the Profile object using the 'pk' from URL parameters
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        # Associate the new status message with the profile
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the profile's detail page after submission
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

