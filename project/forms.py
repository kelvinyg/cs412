from django import forms
from project.models import Group, ItineraryItem, GroupExpense

class CreateGroupForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Trip Start Date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Trip End Date"
    )
    destination = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Destination'}),
        label="Destination"
    )

    class Meta:
        model = Group
        fields = ['name', 'description', 'start_date', 'end_date', 'destination']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after the start date.")
        return cleaned_data


class ItineraryItemForm(forms.ModelForm):
    class Meta:
        model = ItineraryItem
        fields = ['title', 'description', 'date_time', 'location', 'category', 'day']
        widgets = {
            'day': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Day Number'}),
        }



class GroupExpenseForm(forms.ModelForm):
    class Meta:
        model = GroupExpense
        fields = [ 'amount', 'description', 'date', 'split_type']