from django.shortcuts import render
from .models import Group, GroupExpense, Itinerary, Membership, ActivityLog, Split, ItineraryItem
from django.utils.timezone import now  # Import timezone for date filtering
from django.views.generic import ListView, DetailView, TemplateView, CreateView, View, UpdateView, DeleteView
from django.db.models import Q, Sum
from .forms import CreateGroupForm, ItineraryItemForm, GroupExpenseForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.http import Http404
from django.contrib.sites.shortcuts import get_current_site
# Not Used 
import pandas as pd
import json
from django.db.models import Prefetch


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Displays the user's main dashboard shows an overview of:
    - Total groups the user belongs to.
    - Total expenses across all groups.
    - Upcoming trips for groups the user is part of.
    - Recent activity (last 10 actions related to the user or their groups).
    - Expenses owed by the user, grouped by group.
    """
    template_name = 'project/dashboard.html'
    login_url = '/project/login/' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Total groups, expenses, and trips
        context['total_groups'] = Group.objects.filter(membership__user=user).count()
        context['total_expenses'] = GroupExpense.objects.filter(group__membership__user=user).aggregate(total=Sum('amount'))['total'] or 0
        context['upcoming_trips'] = Itinerary.objects.filter(
            group__membership__user=user,  # Ensure the user belongs to the group
            start_date__gte=now()          # Start date in the future or today
        ).distinct().count()  # Avoid duplicate results

        """# Fetch recent activity (last 10 actions involving the user or their groups)
        context['recent_activity'] = ActivityLog.objects.filter(
            Q(user=user) | Q(related_group__membership__user=user)
        ).order_by('-timestamp')[:10]
        """

        context['recent_activity'] = ActivityLog.objects.filter(
            Q(user=user) | Q(related_group__membership__user=user)
        ).distinct().order_by('-timestamp')[:10]

        # Expenses owed per group
        context['expenses_owed'] = (
            Split.objects.filter(user=user, status='unpaid')
            .values('expense__group__id', 'expense__group__name')
            .annotate(total_owed=Sum('amount'))
        )

        return context

class UserGroupsView(LoginRequiredMixin, ListView):
    """
    Displays a list of groups the user belongs to.
    Uses the 'user_groups.html' template with 'memberships' as the context variable to get the groups
    User is associated to.
    """
    template_name = 'project/user_groups.html'
    login_url = '/project/login/' 
    context_object_name = 'memberships'

    def get_queryset(self):
        return Membership.objects.filter(user=self.request.user).select_related('group')

class CreateGroupView(LoginRequiredMixin, CreateView):
    """
    View handles the creation of a new group. By default it will
    - Adds the logged-in user as an admin.
    - Creates an associated itinerary for the group.
    - Logs the creation activity.
    Redirects to the group detail page upon success.
    """
    model = Group
    form_class = CreateGroupForm
    template_name = 'project/create_group.html'
    login_url = '/project/login/' 

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Assign the creator of grouo as admin
        Membership.objects.create(user=self.request.user, group=self.object, role='admin')
        
        # Create the associated itinerary object
        Itinerary.objects.create(
            group=self.object,
            start_date=form.cleaned_data['start_date'],
            end_date=form.cleaned_data['end_date'],
            destination=form.cleaned_data['destination']
        )
        
        # Log the activity object
        ActivityLog.objects.create(
            user=self.request.user,
            action=f"Created group '{self.object.name}'",
            related_group=self.object
        )
        return response

    def get_success_url(self):
        return reverse('group_detail', kwargs={'pk': self.object.id})



class GroupDetailView(DetailView):
    """
    Displays the details of a specific group using group_id:
    - Itinerary items related to the group.
    - Expenses recorded for the group.
    """
    model = Group
    template_name = 'project/group_detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.get_object()

        # Fetch the itinerary items for the grouo
        itinerary_items = ItineraryItem.objects.filter(itinerary__group=group)
        print(f"Fetched Itinerary Items for Group {group.id}: {itinerary_items}")

        context['itinerary_items'] = itinerary_items
        context['expenses'] = GroupExpense.objects.filter(group=group)

        print(context['itinerary_items'])

        return context
    

class AddItineraryItemView(LoginRequiredMixin,CreateView):
    """
    -Handles the addition logic of an itinerary item to a group.
    -Automatically associates the item with the group's itinerary.
    -Adds the user as a member of the group if not already a member.
    -Logs the addition activity.
    """
    model = ItineraryItem
    form_class = ItineraryItemForm
    template_name = 'project/add_itinerary_item.html'

    def form_valid(self, form):
        # Automatically associate the itinerary item with the group
        group = get_object_or_404(Group, pk=self.kwargs['group_id'])
        itinerary, created = group.itineraries.get_or_create(group=group)  # Ensure the group has an itinerary
        form.instance.itinerary = itinerary

        #Assigns a role, failsafe if creator is not admin or role process is lost
        if not Membership.objects.filter(user=self.request.user, group=group).exists():
            Membership.objects.create(user=self.request.user, group=group, role='member')

        #Log Activity object
        ActivityLog.objects.create(
            user=self.request.user,
            action=f"Added itinerary item '{form.instance.title}' for '{itinerary.destination}'",
            related_group=group,
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = get_object_or_404(Group, pk=self.kwargs['group_id'])
        return context

    def get_success_url(self):
        group_id = self.kwargs.get('group_id')  # Retrieve 'group_id' from the URL
        if not group_id:
            raise ValueError("Missing 'group_id' in URL")
        return reverse('group_detail', kwargs={'pk': group_id})
    
class UpdateItineraryItemView(UpdateView):
    """
    View Updates an itinerary item.
    Redirects to the group detail page upon success.
    """
    model = ItineraryItem
    fields = ['title', 'description', 'date_time', 'location', 'category', 'day']
    template_name = 'project/update_itinerary_item.html'

    def get_success_url(self):
        return reverse_lazy('group_detail', kwargs={'pk': self.object.itinerary.group.id})
    
class DeleteItineraryItemView(DeleteView):
    """
    View deletes an itinerary item.
    Redirects to the group detail page upon success.
    """
    model = ItineraryItem
    template_name = 'project/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('group_detail', kwargs={'pk': self.object.itinerary.group.id})
    
class AddExpenseView(CreateView):
    """
    Handles adding logic for an expense for a group:
    - Distributes the expense among group members.
    - Logs the activity.
    Redirects to the group detail page upon success.
    """
    model = GroupExpense
    form_class = GroupExpenseForm
    template_name = 'project/add_expense.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            group_id = self.kwargs.get('group_id')
            context['group'] = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            #Uses Django built in exception, sourced from ChatGPT
            raise Http404("Group not found")
        return context

    def form_valid(self, form):
        # Start a transaction, uses atomic to make sure everything is exectued in a single transaction, 
        # debugged using chatGPT as there would be conflicts for the different models
        with transaction.atomic():
            # Save the expense
            expense = form.save(commit=False)
            expense.group = Group.objects.get(pk=self.kwargs['group_id'])  # Attach the group
            expense.payer = self.request.user  # Set the logged-in user as the payer
            expense.save()

            # Distribute the expense among group members
            group_members = Membership.objects.filter(group=expense.group)
            if not group_members.exists():
                messages.error(self.request, "Cannot create expense as the group has no members.")
                return redirect('group_detail', pk=expense.group.id)

            split_amount = expense.amount / group_members.count()
            for member in group_members:
                Split.objects.create(
                    expense=expense,
                    user=member.user,
                    amount=split_amount,
                    status='unpaid'
                )
            # Log the activity (check for duplicates)
            if not ActivityLog.objects.filter(
                user=self.request.user,
                action__icontains=f"Added expense '{expense.description}'",
                related_group=expense.group,
            ).exists():
                ActivityLog.objects.create(
                    user=self.request.user,
                    action=f"Added expense '{expense.description}'",
                    related_group=expense.group,
                )
            print("Form submitted for expense or itinerary.")
        return redirect('group_detail', pk=expense.group.id)

    def get_success_url(self):
        group_id = self.kwargs.get('group_id')
        return reverse('group_detail', kwargs={'pk': group_id})
    
class UpdateExpenseView(UpdateView):
    """
    Handles the logic of users updating an existing expense.
    Ensures the group associated with the expense cannot be changed during the update.
    Redirects to the group detail page after the update is successful.
    """
    model = GroupExpense
    form_class = GroupExpenseForm
    template_name = 'project/update_expense.html'

    def form_valid(self, form):
        # Access the current expense instance
        instance = form.instance

        # Example: Ensure the group is not modified unintentionally
        instance.group = self.object.group  # Ensure group stays the same

        # Debugging to ensure everything is as expected
        print(f"Updating Expense: {instance}, Group: {instance.group}")

        return super().form_valid(form)

    def get_success_url(self):
        # Use instance.group to construct the URL
        return reverse('group_detail', kwargs={'pk': self.object.group.id})
    
class DeleteExpenseView(DeleteView):
    """
    Allows the user to delete an existing expense.
    Ensures proper redirection after deletion.
    """
    model = GroupExpense
    template_name = 'project/delete_expense.html'

    def get_success_url(self):
        # Ensure the group exists before redirecting
        if not self.object.group:
            messages.error(self.request, "Error: No group associated with this expense.")
            return reverse('user_groups')
        return reverse('group_detail', kwargs={'pk': self.object.group.id})
    

class JoinGroupViaTokenView(LoginRequiredMixin, View):
    """
    Allows users to join a group using a unique invite token.
    If the user is already a member of the group, an error message is shown.
    Otherwise, the user is added to the group as a member.
    Logs the activity and redirects to the group detail page.
    """
    login_url = '/project/login/'  # Redirect for unauthenticated users

    def get(self, request, join_token):
        # Fetch the group associated with the join token
        group = get_object_or_404(Group, join_token=join_token)

        # Generate the invite link logic 
        protocol = "https" if request.is_secure() else "http"
        domain = get_current_site(request).domain
        invite_link = f"{protocol}://{domain}/project/groups/invite/{group.join_token}/"

        # Check if the user is already a member of the group
        if Membership.objects.filter(group=group, user=request.user).exists():
            messages.error(
                request,
                f"You are already a member of the group '{group.name}'. Invite link: {invite_link}"
            )
        else:
            # Add the user to the group
            Membership.objects.create(group=group, user=request.user, role='member')
            messages.success(
                request,
                f"Welcome to the group '{group.name}'! You joined using this invite link: {invite_link}"
            )
        ActivityLog.objects.create(
                user=request.user,
                action=f"Joined the group '{group.name}'",
                related_group=group,
            )
        # Redirect to the group detail page
        return redirect('group_detail', pk=group.id)
    
class GroupExpensesView(DetailView):
    model = Group
    template_name = 'project/group_expenses.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.get_object()

        # Fetch all the expenses for the group
        expenses = GroupExpense.objects.filter(group=group).prefetch_related('splits__user')
        context['expenses'] = expenses

        # Add split details for each expense
        split_details = []
        for expense in expenses:
            payer = expense.payer
            for split in expense.splits.all():
                if split.user != payer:
                    split_details.append({
                        'expense': expense.description,
                        'debtor': split.user.username,
                        'creditor': payer.username,
                        'amount': split.amount,
                        'status': split.status,
                    })
        context['split_details'] = split_details

        # Calculate totals for the dashboard
        total_expenses = sum(expense.amount for expense in expenses)
        total_owed = sum(split.amount for split in Split.objects.filter(expense__group=group, status='unpaid'))
        total_paid = sum(split.amount for split in Split.objects.filter(expense__group=group, status='paid'))

        # Add dashboard totals to the context
        context['total_expenses'] = total_expenses
        context['total_owed'] = total_owed
        context['total_paid'] = total_paid

        return context
    




