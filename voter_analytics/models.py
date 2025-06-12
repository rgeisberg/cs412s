# File: models.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: models file for voter analytics
from django.db import models

# Create your models here.

class Voter(models.Model):
    """model to represent a voter"""
    # Personal Info
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    
    # Address Info
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    
    # Other Info
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=20)
    
    # Participation (0 or 1, or could be BooleanField)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    
    # Numeric score
    voter_score = models.IntegerField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.party_affiliation}) - Precinct {self.precinct_number}"

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    filename = '/Users/rebeccageisberg/Desktop/newton_voters.csv'
    with open(filename, encoding='ISO-8859-1') as f:
        f.readline()  # discard headers

        for line in f:
            fields = line.strip().split(',')

            # Defensive: skip if wrong number of fields
            if len(fields) < 17:
                print(f"Skipped line (not enough fields): {fields}")
                continue

            try:
                voter = Voter(
                    last_name = fields[1],
                    first_name = fields[2],
                    street_number = fields[3],
                    street_name = fields[4],
                    apartment_number = fields[5],
                    zip_code = fields[6],
                    date_of_birth = fields[7],
                    date_of_registration = fields[8],
                    party_affiliation = fields[9].strip(),  # remove extra spaces
                    precinct_number = fields[10],
                    v20state = fields[11].upper() == "TRUE",
                    v21town = fields[12].upper() == "TRUE",
                    v21primary = fields[13].upper() == "TRUE",
                    v22general = fields[14].upper() == "TRUE",
                    v23town = fields[15].upper() == "TRUE",
                    voter_score = int(fields[16]),
                )
                voter.save()
                print(f'Created voter: {voter}')

            except Exception as e:
                print(f"Skipped: {fields}\nError: {e}")

    print(f'Done. Created {Voter.objects.count()} Voters.')
