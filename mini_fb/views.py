from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, Image, StatusMessage, Friend
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



# Views accessible to everyone (no login required)
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        # Check if 'pk' is provided in the URL kwargs
        if 'pk' in self.kwargs:
            # Fetch the profile for the specified pk
            return get_object_or_404(Profile, pk=self.kwargs['pk'])
        else:
            # Otherwise, fetch the logged-in user's profile
            return get_object_or_404(Profile, user=self.request.user)


class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            form.instance.user = user  # Attach the user to the profile

            # Optionally, log in the user immediately after registration
            login(self.request, user)

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


# Views requiring login for modifying database entries
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.profile = profile
        sm = form.save()
        files = self.request.FILES.getlist('files')
        for file in files:
            image = Image(image_file=file, status_message=sm)
            image.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile')


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)


class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'delete'

    def get_success_url(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return reverse('show_profile')


class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    form_class = UpdateStatusForm
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return reverse('show_profile')


class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        # Get the logged-in user's Profile
        profile = get_object_or_404(Profile, user=request.user)
        # Get the other user's Profile to be added as a friend
        other_profile = get_object_or_404(Profile, pk=kwargs['other_pk'])

        # Call the add_friend method on the current profile
        profile.add_friend(other_profile)

        # Redirect to the profile page
        return redirect('show_profile')


class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context


class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_feed'] = self.object.get_news_feed()
        return context