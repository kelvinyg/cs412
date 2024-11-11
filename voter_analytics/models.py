import csv
from datetime import datetime
from django.db import models
from django.conf import settings
import os


# Create your models here.
class Voter(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)

    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50, help_text="Political party affiliation")
    precinct_number = models.CharField(max_length=20)
    
    # Voting History for Recent Elections
    v20_state = models.BooleanField(default=False, help_text="Voted in 2020 State Election")
    v21_town = models.BooleanField(default=False, help_text="Voted in 2021 Town Election")
    v21_primary = models.BooleanField(default=False, help_text="Voted in 2021 Primary Election")
    v22_general = models.BooleanField(default=False, help_text="Voted in 2022 General Election")
    v23_town = models.BooleanField(default=False, help_text="Voted in 2023 Town Election")

    # Calculated Voting Score (Participation in Past Elections)
    voter_score = models.IntegerField(help_text="Number of past 5 elections the voter participated in")
    
    # String Representation
    def __str__(self):
        return f"{self.first_name} {self.last_name}, Precinct {self.precinct_number}, Party: {self.party_affiliation}"
    
    @staticmethod
    def load_data(file_path=None):
        """Load voter data from a CSV file into the database."""
        if file_path is None:
            file_path = os.path.join(settings.BASE_DIR, 'newton_voters.csv')

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert 'TRUE'/'FALSE' to boolean values
                def to_bool(value):
                    return value.strip().upper() == 'TRUE'
                
                # Create and save each Voter instance
                Voter.objects.create(
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    street_number=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apartment_number=row.get('Residential Address - Apartment Number', None),
                    zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                    date_of_registration=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                    party_affiliation=row['Party Affiliation'],
                    precinct_number=row['Precinct Number'],
                    v20_state=to_bool(row['v20state']),
                    v21_town=to_bool(row['v21town']),
                    v21_primary=to_bool(row['v21primary']),
                    v22_general=to_bool(row['v22general']),
                    v23_town=to_bool(row['v23town']),
                    voter_score=int(row['voter_score'])
                )
