from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, Image
from django.urls import reverse
from .forms import *
from django.shortcuts import get_object_or_404, redirect




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

        sm = form.save()
        files = self.request.FILES.getlist('files')

        for file in files:
            image = Image(image_file=file, status_message= sm)
            image.save()

        
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the profile's detail page after submission
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'


class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'delete'

    def get_success_url(self):
        # Get the profile associated with the StatusMessage
        profile_id = self.object.profile.pk
        # Redirect to the profile's page after deletion
        return reverse('show_profile', kwargs={'pk': profile_id})

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    form_class = UpdateStatusForm
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        # After updating, redirect back to the profile page associated with the status
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})


class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        # Get the primary keys from the URL parameters
        pk = kwargs.get('pk')
        other_pk = kwargs.get('other_pk')

        # Get the Profile instances for both the current user and the friend to be added
        profile = get_object_or_404(Profile, pk=pk)
        other_profile = get_object_or_404(Profile, pk=other_pk)

        # Call the add_friend method on the current profile
        profile.add_friend(other_profile)

        # Redirect to the profile page (you can customize the redirect as needed)
        return redirect('show_profile', pk=pk)
    
class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve friend suggestions for the profile
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context
    

class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the news feed to the context
        context['news_feed'] = self.object.get_news_feed()
        return context
    

    