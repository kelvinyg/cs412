from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
import plotly.express as px
from django.utils.safestring import mark_safe
import pandas as pd

# Create your views here.
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()
        party_affiliation = self.request.GET.get('party_affiliation')
        min_birth_year = self.request.GET.get('min_birth_year')
        max_birth_year = self.request.GET.get('max_birth_year')
        voter_score = self.request.GET.get('voter_score')
        voted_in_20_state = self.request.GET.get('v20_state')
        voted_in_21_town = self.request.GET.get('v21_town')
        voted_in_21_primary = self.request.GET.get('v21_primary')
        voted_in_22_general = self.request.GET.get('v22_general')
        voted_in_23_town = self.request.GET.get('v23_town')

        # Filter by party affiliation
        if party_affiliation:
            queryset = queryset.filter(party_affiliation=party_affiliation)

        # Filter by date of birth range
        if min_birth_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_birth_year))
        if max_birth_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_birth_year))

        # Filter by voter score
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))

        # Filter by specific election participation
        if voted_in_20_state:
            queryset = queryset.filter(v20_state=True)
        if voted_in_21_town:
            queryset = queryset.filter(v21_town=True)
        if voted_in_21_primary:
            queryset = queryset.filter(v21_primary=True)
        if voted_in_22_general:
            queryset = queryset.filter(v22_general=True)
        if voted_in_23_town:
            queryset = queryset.filter(v23_town=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct()
        context['years'] = list(range(1900, 2024))  # Adjust year range as needed
        return context
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'




class GraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        queryset = Voter.objects.all()

        # Get filter parameters from GET request
        party_affiliation = self.request.GET.get('party_affiliation')
        min_birth_year = self.request.GET.get('min_birth_year')
        max_birth_year = self.request.GET.get('max_birth_year')
        voter_score = self.request.GET.get('voter_score')
        voted_in_20_state = self.request.GET.get('v20_state')
        voted_in_21_town = self.request.GET.get('v21_town')
        voted_in_21_primary = self.request.GET.get('v21_primary')
        voted_in_22_general = self.request.GET.get('v22_general')
        voted_in_23_town = self.request.GET.get('v23_town')

        # Apply filters if they are set
        if party_affiliation:
            queryset = queryset.filter(party_affiliation=party_affiliation)
        if min_birth_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_birth_year))
        if max_birth_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_birth_year))
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        if voted_in_20_state:
            queryset = queryset.filter(v20_state=True)
        if voted_in_21_town:
            queryset = queryset.filter(v21_town=True)
        if voted_in_21_primary:
            queryset = queryset.filter(v21_primary=True)
        if voted_in_22_general:
            queryset = queryset.filter(v22_general=True)
        if voted_in_23_town:
            queryset = queryset.filter(v23_town=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        # Load filtered data into a DataFrame
        voters_data = queryset.values('date_of_birth', 'party_affiliation', 'v20_state', 'v21_town', 'v21_primary', 'v22_general', 'v23_town')
        df = pd.DataFrame.from_records(voters_data)

        # 1. Histogram of Voters by Year of Birth
        if not df.empty:
            df['birth_year'] = pd.to_datetime(df['date_of_birth']).dt.year
            birth_year_count = df['birth_year'].value_counts().sort_index().reset_index()
            birth_year_count.columns = ['Year of Birth', 'Count']
            
            fig_birth_year = px.bar(
                birth_year_count, x='Year of Birth', y='Count', 
                title='Distribution of Voters by Year of Birth'
            )
            fig_birth_year.update_layout(xaxis_title='Year of Birth', yaxis_title='Number of Voters')
            context['birth_year_chart'] = mark_safe(fig_birth_year.to_html(full_html=False, include_plotlyjs='cdn'))
        else:
            context['birth_year_chart'] = "<p>No data available for this filter selection.</p>"

        # 2. Pie Chart of Voters by Party Affiliation
        if not df['party_affiliation'].empty:
            party_affiliation_count = df['party_affiliation'].value_counts().reset_index()
            party_affiliation_count.columns = ['Party Affiliation', 'Count']

            fig_party_affiliation = px.pie(
                party_affiliation_count, names='Party Affiliation', values='Count',
                title='Distribution of Voters by Party Affiliation'
            )
            fig_party_affiliation.update_layout(width=600, height=600)
            context['party_affiliation_chart'] = mark_safe(fig_party_affiliation.to_html(full_html=False, include_plotlyjs='cdn'))
        else:
            context['party_affiliation_chart'] = "<p>No data available for this filter selection.</p>"

        # 3. Histogram of Voter Participation by Election
        if not df.empty:
            election_counts = {
                '2020 State Election': df['v20_state'].sum(),
                '2021 Town Election': df['v21_town'].sum(),
                '2021 Primary Election': df['v21_primary'].sum(),
                '2022 General Election': df['v22_general'].sum(),
                '2023 Town Election': df['v23_town'].sum()
            }
            election_df = pd.DataFrame(list(election_counts.items()), columns=['Election', 'Count'])

            fig_election_participation = px.bar(
                election_df, x='Election', y='Count', 
                title='Voter Participation in Each Election'
            )
            fig_election_participation.update_layout(xaxis_title='Election', yaxis_title='Number of Voters')
            context['election_participation_chart'] = mark_safe(fig_election_participation.to_html(full_html=False, include_plotlyjs='cdn'))
        else:
            context['election_participation_chart'] = "<p>No data available for this filter selection.</p>"

        # Add form options to the context
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct()
        context['years'] = list(range(1900, 2024))  # Adjust the year range as needed

        return context