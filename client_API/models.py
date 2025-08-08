from django.db import models
from home_API.models import Area, Units


class Client(models.Model):
    fname = models.CharField(max_length=100, blank=True, null=True)
    lname = models.CharField(max_length=100, blank=True,null=True)
    phoneNO = models.PositiveBigIntegerField(blank=True, null=True,default=0)
    massageNO = models.PositiveBigIntegerField(blank=True, null=True,default=0)
    email = models.EmailField(blank=True, null=True)
    added_by = models.ForeignKey('organization.Employee', on_delete=models.SET_NULL, related_name='added_clients', null=True, blank=True)
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='clients', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    # assigned_to = models.ForeignKey('organization.Employee', on_delete=models.SET_NULL, related_name='assigned_clients', null=True, blank=True)
    assignees_to = models.ManyToManyField('organization.Employee', related_name='assigned_clients', null=True, blank=True)
    status = models.CharField(max_length=100,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'In Active'),
                                  ('sold', 'Sold'),
                              ),
                              default='active',)

    def __str__(self):
        return f"{self.fname} {self.lname}"


class SearchFilter(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    Area = models.ManyToManyField(Area, null=True, blank=True)
    startBudget = models.FloatField()
    stopBudget = models.FloatField()
    startCarpetArea = models.FloatField()
    stopCarpetArea = models.FloatField()
    possession = models.DateTimeField()
    requirements = models.CharField(max_length=200, blank=True, null=True)
    units = models.ManyToManyField(Units, null=True, blank=True)

    # Add fields for specific search criteria (e.g., location, price range, category, etc.)

    def __str__(self):
        return f"{self.client.fname} {self.client.lname}"


class FollowUp(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    message = models.TextField()
    actions = models.CharField(max_length=100)
    date_sent = models.DateTimeField()
    done = models.BooleanField(default=False)
    added_by = models.ForeignKey('organization.Employee', on_delete=models.SET_NULL, related_name='follow_ups', null=True, blank=True)

    def __str__(self):
        return f"{self.client.fname} {self.client.lname} - {self.date_sent}"


class Feedback(models.Model):
    follow_up = models.ForeignKey(FollowUp, on_delete=models.CASCADE)
    response = models.CharField(max_length=100)
    message = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.follow_up}- Feedback"
