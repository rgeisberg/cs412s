# File: views.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: views file for voter analytics
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Min, Max, Q, Count
from django.db import models
import plotly.graph_objs as go
import plotly.offline


class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'   
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset()
        party = self.request.GET.get('party', '')
        min_dob = self.request.GET.get('min_dob', '')
        max_dob = self.request.GET.get('max_dob', '')
        score = self.request.GET.get('score', '')
        name_search = self.request.GET.get('name_search', '').strip()
        if name_search:
            # Split on whitespace, search for each part in either field (case-insensitive)
            parts = name_search.split()
            for part in parts:
                qs = qs.filter(models.Q(first_name__icontains=part) | models.Q(last_name__icontains=part))
        if party:
            qs = qs.filter(party_affiliation=party)
        if min_dob:
            qs = qs.filter(date_of_birth__year__gte=int(min_dob))
        if max_dob:
            qs = qs.filter(date_of_birth__year__lte=int(max_dob))
        if score:
            qs = qs.filter(voter_score=int(score))
        for election in ['v20state','v21town','v21primary','v22general','v23town']:
            if self.request.GET.get(election):
                qs = qs.filter(**{election: True})
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['party_choices'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        # All possible years in your data:
        year_min = Voter.objects.aggregate(m=Min('date_of_birth'))['m'].year
        year_max = Voter.objects.aggregate(m=Max('date_of_birth'))['m'].year
        ctx['year_choices'] = list(range(year_min, year_max + 1))
        ctx['score_choices'] = sorted(Voter.objects.values_list('voter_score', flat=True).distinct())
        ctx['name_search'] = self.request.GET.get('name_search', '')
        return ctx
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


class VoterGraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        qs = super().get_queryset()
        # Filters:
        party = self.request.GET.get('party', '')
        min_dob = self.request.GET.get('min_dob', '')
        max_dob = self.request.GET.get('max_dob', '')
        score = self.request.GET.get('score', '')
        if party:
            qs = qs.filter(party_affiliation=party)
        if min_dob:
            qs = qs.filter(date_of_birth__year__gte=int(min_dob))
        if max_dob:
            qs = qs.filter(date_of_birth__year__lte=int(max_dob))
        if score:
            qs = qs.filter(voter_score=int(score))
        for election in ['v20state','v21town','v21primary','v22general','v23town']:
            if self.request.GET.get(election):
                qs = qs.filter(**{election: True})
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = context['voters']

        # For the filter form (choices):
        context['party_choices'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        year_min = Voter.objects.aggregate(m=Min('date_of_birth'))['m'].year
        year_max = Voter.objects.aggregate(m=Max('date_of_birth'))['m'].year
        context['year_choices'] = list(range(year_min, year_max + 1))
        context['score_choices'] = sorted(Voter.objects.values_list('voter_score', flat=True).distinct())
        context['request'] = self.request

        # --- Graph 1: Birth Year Histogram ---
        years = [v.date_of_birth.year for v in voters if v.date_of_birth]
        fig1 = go.Histogram(x=years, nbinsx=15)
        graph_div_birth_year = plotly.offline.plot(
            {"data": [fig1], "layout_title_text": "Distribution by Year of Birth"},
            auto_open=False, output_type="div"
        )
        context['graph_birth_year'] = graph_div_birth_year

        # --- Graph 2: Party Affiliation Pie Chart ---
        # Normalize party labels (strip, uppercase, set blank to "Unknown")
        party_counts = {}
        for v in voters:
            p = (v.party_affiliation or '').strip().upper()
            if not p:
                p = "Unknown"
            party_counts[p] = party_counts.get(p, 0) + 1

        fig2 = go.Pie(
            labels=list(party_counts.keys()),
            values=list(party_counts.values()),
            textinfo="percent+label",  # only show percent and label on the chart
            insidetextorientation='auto',  # keep text readable
            hole=0,  # 0 for a regular pie (set >0 for donut)
        )
        

        graph_div_party = plotly.offline.plot(
            {"data": [fig2], "layout_title_text": "Distribution by Party Affiliation"},
            auto_open=False, output_type="div"
        )
        context['graph_party'] = graph_div_party

        # --- Graph 3: Participation in Each Election ---
        election_labels = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']
        election_fields = ['v20state','v21town','v21primary','v22general','v23town']
        counts = [voters.filter(**{e: True}).count() for e in election_fields]
        fig3 = go.Bar(x=election_labels, y=counts)
        graph_div_participation = plotly.offline.plot(
            {"data": [fig3], "layout_title_text": "Participation in Elections"},
            auto_open=False, output_type="div"
        )
        context['graph_participation'] = graph_div_participation

        return context
