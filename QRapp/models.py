from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Exhibit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    name_ml = models.CharField(max_length=255, verbose_name=_('Name in Malayalam'), null=False, )
    description_ml = models.TextField(verbose_name=_('Description in Malayalam'), null=False, blank=False)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    image_ids = models.CharField(max_length=255)
    qr_code_image = models.ImageField(upload_to='qr_codes/')  # QR code image

    def __str__(self):
        return self.name

    def set_image_ids(self, image_ids):
        self.image_ids = ','.join(str(id) for id in image_ids)
        self.save()

    def get_image_ids(self):
        return [int(id) for id in self.image_ids.split(',')] if self.image_ids else []
    
    def delete(self, *args, **kwargs):
        # Delete the QR code image file if it exists
        if self.qr_code_image:
            self.qr_code_image.delete(save=False)

        # Delete all associated images
        for image in self.images.all():
            image.delete()  # This will call the delete method of the Image model

        super().delete(*args, **kwargs)


class Image(models.Model):
    exhibit = models.ForeignKey(Exhibit, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='exhibits/')
    caption = models.TextField(blank=True, null=True) 
    caption_ml = models.TextField(blank=True, null=True)  # Malayalam caption
    position = models.PositiveIntegerField(default=0)  # New field for ordering

    class Meta:
        ordering = ['position']  # Default ordering by position

    def __str__(self):
        return f"Image for {self.exhibit.name} - {self.caption or 'No Caption'}"

    def delete(self, *args, **kwargs):
        # Delete the image file from the filesystem
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)

class Event(models.Model):
    EVENT_TYPES = [
        ('Competition', 'Competition'),
        ('Workshop', 'Workshop'),
        ('Meetup', 'Meetup'),
        ('Event', 'Event')
    ]
    
    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/')  # Ensure this is the correct field name
    location = models.CharField(max_length=200)
    duration = models.DurationField()
    event_time = models.TimeField()
    organizer = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        # Delete the event image file if it exists
        if self.image:
           self.image.delete(save=False)
        super().delete(*args, **kwargs) 
          
class EventApplication(models.Model):
    USER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('school', 'School'),
        ('high school', 'high school'),
        ('academy', 'academy'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  # Individual name or school name
    phone_no = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    members = models.IntegerField(default=1)
    applied_on = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='individual')

    # New Fields for Schools
    student_names = models.TextField(blank=True, null=True)  # Comma-separated student names
    student_phones = models.TextField(blank=True, null=True)  # Comma-separated phone numbers
    student_classes = models.TextField(blank=True, null=True)  # Comma-separated class details

    def __str__(self):
        return f"{self.name} applied for {self.event.name}"
