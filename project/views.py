from django.shortcuts import render
# File: views.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: views file for recipe

from django.views.generic import *
from .models import *
from .forms import *
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.shortcuts import redirect

class ShowAllRecipes(ListView):
    """view to show all recipes"""
    model = Recipe
    template_name = 'project/show_all_recipes.html'  # customize as needed
    context_object_name = 'recipes'
    ordering = ['-date_added']  # newest first

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.query  # pass query directly
        return context

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        self.query = query  # store for use in context
        qs = Recipe.objects.all().order_by('-date_added')
        if query:
            qs = qs.filter(title__icontains=query)
        return qs

class RecipeDetailView(DetailView):
    """view each recipe in detail"""
    model = Recipe
    template_name = 'project/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = CommentReview.objects.filter(recipe=self.object).order_by('-date_posted')
        context["form"] = CommentReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentReviewForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = self.object
            profile, created = Profile.objects.get_or_create(user=request.user)
            comment.profile = profile
            comment.date_posted = now()
            comment.save()
            return redirect('recipe_detail', pk=self.object.pk)
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class CustomLoginView(LoginView):
    template_name = 'project/login.html'

    def get_success_url(self):
        return  '/project/recipes/'
    

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = "project/signup_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = CustomUserCreationForm()
        return context

    def form_valid(self, form):
        user_form = CustomUserCreationForm(self.request.POST)

        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user)
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, user_creation_form=user_form)
            )


    def get_success_url(self):
        return '/project/recipes/'


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'project/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.recipe_profile
        context['profile'] = profile  
        context['saved_recipes'] = Recipe.objects.filter(savedrecipie__profile=profile)
        return context
    
class SaveRecipeView(LoginRequiredMixin, View):
    """Handle saving a recipe to a user's profile"""

    def post(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
            profile = Profile.objects.get(user=request.user)

            SavedRecipie.objects.get_or_create(
                profile=profile,
                recipe=recipe,
                defaults={'saved_at_time': now()}
            )

        except (Recipe.DoesNotExist, Profile.DoesNotExist):
            # You could log this or show a message if desired
            pass
        return redirect(reverse('profile'))