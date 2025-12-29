from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('House', 'House'),
        ('Land', 'Land'),
    ]

    STATUS_CHOICES = [
        ('For Sale', 'For Sale'),
        ('For Rent', 'For Rent'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    # Fields specific to houses (can be null for land)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)

    area_sqft = models.IntegerField()
    location = models.CharField(max_length=255)

    # For land-specific details like "Facing South"
    facing = models.CharField(max_length=50, null=True, blank=True)

    main_image = models.ImageField(upload_to='properties/%Y/%m/%d/')
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='properties/%Y/%m/%d/')

    def __str__(self):
        return f"Image for {self.property.title} ({self.id})"


class MessageModel(models.Model):
    """
    Represents a message within a conversation thread.
    """
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    # This field links a reply to the first message in the conversation
    parent_message = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"

    class Meta:
        ordering = ['timestamp']  # Show oldest messages first in a thread
