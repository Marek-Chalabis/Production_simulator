import datetime
import math
import uuid

import phonenumbers
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


def validate_zero(value):
    if value < 0:
        raise ValidationError('Parameter cannot be less then 0')


class Producers(models.Model):
    producer_id = models.AutoField(primary_key=True)
    producer_name = models.CharField(unique=True, max_length=30)
    contact_person = models.CharField(max_length=50)
    phone_number = PhoneNumberField(blank=False, unique=True, default='+48')
    email = models.CharField(max_length=50, blank=True, null=True)
    rabat = models.DecimalField(max_digits=4, decimal_places=2, validators=[validate_zero])
    delivery_time_days = models.CharField(max_length=15, default='-')

    def get_absolute_url(self):
        return reverse('producer-detail', kwargs={'pk': self.pk})

    def formatted_phone_number(self):
        return phonenumbers.format_number(self.phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

    def __str__(self):
        return self.producer_name

    class Meta:
        managed = True
        db_table = 'producers'


class Positions(models.Model):
    position_id = models.AutoField(primary_key=True)
    position_name = models.CharField(max_length=30)
    hourly_rate = models.FloatField()

    def __str__(self):
        return self.position_name

    class Meta:
        managed = False
        db_table = 'positions'


class Employees(models.Model):
    uuid_employee = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone_number = PhoneNumberField(blank=False, unique=True, default='+48')
    position = models.ForeignKey(Positions, on_delete=models.PROTECT, default=1)
    date_of_employment = models.DateField(default=datetime.date.today)

    def get_absolute_url(self):
        return reverse('employee-detail', kwargs={'pk': self.pk})

    def formatted_phone_number(self):
        return phonenumbers.format_number(self.phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}({self.position})"

    class Meta:
        managed = False
        db_table = 'employees'


class Projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(unique=True, max_length=30)
    time_for_project_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                                 validators=[validate_zero])
    profit = models.DecimalField(max_digits=15, decimal_places=2, validators=[validate_zero])
    employees = models.ManyToManyField(Employees, through='EmployeesInProjects')

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.project_name)

    class Meta:
        managed = True
        db_table = 'projects'


class EmployeesInProjects(models.Model):
    connection_id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, db_column='uuid_employee')

    def __str__(self):
        return self.connection_id

    class Meta:
        managed = True
        db_table = 'employees_in_projects'


class Tools(models.Model):
    tool_id = models.BigAutoField(primary_key=True)
    geometry = models.CharField(max_length=20, choices=(
        ('Square', 'Square'), ('Ball', 'Ball'), ('Corner radius', 'Corner radius')))
    material = models.CharField(max_length=20,
                                choices=(('VHM', 'VHM'), ('HSS', 'HSS'), ('HSS-E', 'HSS-E')))
    diameter_mm = models.DecimalField(max_digits=5, decimal_places=2, validators=[validate_zero])
    shank_diameter_mm = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True,
                                            validators=[validate_zero])
    tool_radius_mm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                         validators=[validate_zero])
    tool_length_mm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                         validators=[validate_zero])
    working_part_length_mm = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True,
                                                 validators=[validate_zero])
    compensation_mm = models.FloatField(blank=True, null=True, validators=[validate_zero])
    producer = models.ForeignKey(Producers, on_delete=models.SET_DEFAULT, default=1)
    status = models.CharField(max_length=20, choices=(
        ('Can be_use', 'Can be use'), ('Needs sharpening', 'Needs sharpening'), ('Utilize the tool', (
            'Utilize the tool'))), default='Can be use')
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[validate_zero])
    date_of_purchase = models.DateField(default=datetime.date.today)
    project = models.ForeignKey(Projects, default=1, on_delete=models.SET_DEFAULT)

    def get_absolute_url(self):
        return reverse('tool-detail', kwargs={'pk': self.pk})

    def clean(self):
        if self.tool_radius_mm is not None:
            if self.tool_radius_mm > self.diameter_mm / 2:
                raise ValidationError('Tool radius needs to be less or equal to 1/2 * Diameter')
            elif self.geometry == 'Square' and self.tool_radius_mm != 0:
                raise ValidationError('A tool with "Square" geometry cannot have a radius')
            elif self.geometry == 'Ball' and (self.diameter_mm / 2) != self.tool_radius_mm:
                raise ValidationError('A tool with "Ball" geometry cannot have a Radius different then 1/2 * Diameter')

        elif self.geometry == 'Corner_radius' and (self.tool_radius_mm == 0 or self.tool_radius_mm is None):
            raise ValidationError('A tool with "Corner radius" geometry must have a radius')

        elif (self.tool_length_mm and self.working_part_length_mm) is not None:
            if self.tool_length_mm < self.working_part_length_mm:
                raise ValidationError('Tool length cannot be less then working part')

        elif self.compensation_mm is not None:
            if self.compensation_mm > self.tool_radius_mm / 2:
                raise ValidationError('Tool compensation cannot be more then tool radius')

    def __str__(self):
        return f'ID: {self.tool_id} GEOMETRY: {self.geometry} MATERIAL: {self.material} ' \
               f'DIAMETER: {self.diameter_mm} RADIUS: {self.tool_radius_mm}'

    def save(self, *args, **kwargs):
        self.shank_diameter_mm = self.shank_diameter_mm if self.shank_diameter_mm else math.ceil(self.diameter_mm)
        self.compensation_mm = self.compensation_mm if self.compensation_mm else 0
        self.tool_radius_mm = 0 if self.geometry == 'Square' \
            else self.diameter_mm / 2 if self.geometry == 'Ball' \
            else self.tool_radius_mm
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'tools'
