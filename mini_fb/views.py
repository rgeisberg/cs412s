# File: views.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: views file for mini_fb
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, Image, StatusImage, StatusMessage, Friend
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateMessageForm
from django.urls import reverse 

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

class CreateStatusMessageView(CreateView):
    """Define a view class to create status messages"""
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

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
    


    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the profile) to the status
        object before saving it to the database.
        '''

		# instrument our code to display form fields: 
        print(f"CreateStatusMessageView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # attach this profile to the status message
        form.instance.profile = profile # set the FK

        # save the status message to database
        sm = form.save()

        # read the file from the form:
        files = self.request.FILES.getlist('files')

        for file in files:
            image = Image(image_file=file, profile=profile)
            image.save()
            status_image = StatusImage(status_message=sm, image=image)
            status_image.save()

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new status message.'''

        # create and return a URL:
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this profile
        return reverse('profile', kwargs={'pk':pk})

class UpdateProfileView(UpdateView):
    """view class to update a profile"""
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

class DeleteStatusMessageView(DeleteView):
    """view class to delete status message"""
    model = StatusMessage
    template_name = "mini_fb/delete_status_message.html"
    context_object_name = 'status_message'

    def get_success_url(self):
        """route to url after success"""
        return reverse('profile', kwargs={'pk': self.object.profile.pk})
    
class UpdateStatusMessageView(UpdateView):
    """view class to update status message"""
    model = StatusMessage
    template_name = "mini_fb/update_status_message.html"
    form_class = UpdateMessageForm
    context_object_name = 'status_message'

    def get_success_url(self):
        """route to url after success"""
        return reverse('profile', kwargs={'pk': self.object.profile.pk})

class AddFriendView(View):
    """view class to add a friend"""
    
    def dispatch(self, request, *args, **kwargs):
        self_profile = Profile.objects.get(pk=kwargs['pk'])
        other_profile = Profile.objects.get(pk=kwargs['other_pk'])
        self_profile.add_friend(other_profile)
        return redirect(reverse('profile', kwargs={'pk': self_profile.pk}))
    
class ShowFriendSuggestionsView(View):
    """view class to show friend suggestions"""

    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=kwargs['pk'])
        return render(request, 'mini_fb/friend_suggestions.html', {
            'profile': profile,
        })

class ShowNewsFeedView(DetailView):
    """Defind a view class to show one profile"""
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile' 

    




