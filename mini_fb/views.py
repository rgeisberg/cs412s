# File: views.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: views file for mini_fb
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from .models import Profile, Image, StatusImage, StatusMessage, Friend
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateMessageForm
from django.urls import reverse 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

class ShowAllProfilesView(ListView):
    """Define a view class to show all profiles"""
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfile(DetailView):
    """Defind a view class to show one profile"""
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    """Define a view class to create profiles"""
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_creation_form = UserCreationForm()
        context['user_creation_form'] = user_creation_form
        return context
    
    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user)
            form.instance.user = user
            return super().form_valid(form)
        else:
            print("UserCreationForm errors:", user_form.errors)
            return self.render_to_response(
                self.get_context_data(form=form, user_creation_form=user_form)
            )

        

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    """Define a view class to create status messages"""
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context
    
    def get_object(self):
        """get pk not from url but from obj"""
        return Profile.objects.get(user=self.request.user)
    


    def form_valid(self, form):
        '''Handles form submission and saves the new StatusMessage to the DB.'''

        print(f"CreateStatusMessageView.form_valid: form.cleaned_data={form.cleaned_data}")

        # Get the profile based on the logged-in user
        profile = Profile.objects.get(user=self.request.user)

        # Attach this profile to the status message
        form.instance.profile = profile

        # Save the status message
        sm = form.save()

        # Save any uploaded images
        files = self.request.FILES.getlist('files')
        for file in files:
            image = Image(image_file=file, profile=profile)
            image.save()
            status_image = StatusImage(status_message=sm, image=image)
            status_image.save()

        # Continue with normal processing
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new status message.'''
        
        profile = Profile.objects.get(user=self.request.user)
        return reverse('profile', kwargs={'pk': profile.pk})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """view class to update a profile"""
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_object(self):
        """get pk not from url but from obj"""
        return Profile.objects.get(user=self.request.user)

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    """view class to delete status message"""
    model = StatusMessage
    template_name = "mini_fb/delete_status_message.html"
    context_object_name = 'status_message'

    def get_success_url(self):
        """route to url after success"""
        return reverse('profile', kwargs={'pk': self.object.profile.pk})
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    """view class to update status message"""
    model = StatusMessage
    template_name = "mini_fb/update_status_message.html"
    form_class = UpdateMessageForm
    context_object_name = 'status_message'

    def get_success_url(self):
        """route to url after success"""
        return reverse('profile', kwargs={'pk': self.object.profile.pk})

class AddFriendView(LoginRequiredMixin, View):
    """view class to add a friend"""
    
    def dispatch(self, request, *args, **kwargs):
        self_profile = Profile.objects.get(user=request.user)
        other_profile = Profile.objects.get(pk=kwargs['other_pk'])

        self_profile.add_friend(other_profile)

        return redirect(reverse('profile', kwargs={'pk': self_profile.pk}))

    
    def get_object(self):
        """get pk not from url but from obj"""
        return Profile.objects.get(user=self.request.user)
    
class ShowFriendSuggestionsView(LoginRequiredMixin, View):
    """view class to show friend suggestions"""

    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        return render(request, 'mini_fb/friend_suggestions.html', {
            'profile': profile,
        })

    def get_object(self):
        """get pk not from url but from obj"""
        return Profile.objects.get(user=self.request.user)

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    """Defind a view class to show one profile"""
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        """get pk not from url but from obj"""
        return Profile.objects.get(user=self.request.user) 

class CustomLoginRequiredMixin(LoginRequiredMixin):
    """view class custom require login"""
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the  profile to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add this profile into the context dictionary:
        context['profile'] = profile
        return context
    
    def get_login_url(self):
        return reverse('login')
        
class LogoutConfirmationView(TemplateView):
    """view to show custom logout"""
    template_name = 'mini_fb/logged_out.html'
    model = Profile




