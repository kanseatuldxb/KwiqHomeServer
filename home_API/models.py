import os

from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    area = models.CharField(max_length=100)
    projectName = models.CharField(max_length=100)
    projectType = models.CharField(max_length=100)
    developerName = models.CharField(max_length=100)
    landParcel = models.FloatField()
    landmark = models.CharField(max_length=100)
    areaIn = models.CharField(max_length=100)
    waterSupply = models.CharField(max_length=100)
    floors = models.IntegerField()
    flatsPerFloors = models.IntegerField()
    totalUnit = models.IntegerField()
    availableUnit = models.IntegerField()
    amenities = models.CharField(max_length=100)
    parking = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    transport = models.BooleanField()
    readyToMove = models.BooleanField()
    power = models.BooleanField()
    goods = models.BooleanField()
    rera = models.DateTimeField()
    possession = models.DateTimeField()
    contactPerson = models.CharField(max_length=100)
    contactNumber = models.PositiveBigIntegerField()
    marketValue = models.IntegerField()
    lifts = models.IntegerField()
    brokerage = models.FloatField()
    incentive = models.IntegerField()
    url = models.CharField(max_length=200, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey('organization.Employee', on_delete=models.SET_NULL, related_name='added_projects',
                                 null=True, blank=True)
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='projects',
                                     null=True, blank=True)
    def __str__(self):
        return f'{self.projectName} {self.area}'


class Units(models.Model):
    value = models.FloatField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Unit(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='units')
    unit = models.FloatField()
    CarpetArea = models.IntegerField()
    price = models.IntegerField()
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='units',
                                     null=True, blank=True)
    def __str__(self):
        return f"{self.unit} {self.project_id.projectName}"


class GovernmentalArea(models.Model):
    name = models.CharField(max_length=100)
    formatted_version = models.CharField(max_length=100, unique=True, primary_key=True)

    def save(self, *args, **kwargs):
        # Generate formatted version of the name before saving
        self.formatted_version = slugify(self.name.replace(" ", ""))
        super(GovernmentalArea, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=100)
    formatted_version = models.CharField(max_length=100, unique=True, primary_key=True)

    def save(self, *args, **kwargs):
        # Generate formatted version of the name before saving
        self.formatted_version = slugify(self.name.replace(" ", ""))
        super(Area, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Images/')
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        # Delete the image file from the file system before deleting the model instance
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)


class FloorMap(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Images/FloorMap/')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        # Delete the image file from the file system before deleting the model instance
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
