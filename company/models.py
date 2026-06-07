from django.db import models


class ContactMessage(models.Model):
    name         = models.CharField(max_length=100)
    email        = models.EmailField()
    phone        = models.CharField(max_length=50, blank=True)
    subject      = models.CharField(max_length=200, blank=True)
    message      = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.name} - {self.subject or "No subject"}'


class CompanyProfile(models.Model):
    catalogue     = models.FileField(upload_to='catalogue/', blank=True, null=True)
    email         = models.EmailField(blank=True)
    phone         = models.CharField(max_length=50, blank=True)
    address       = models.TextField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    map_link      = models.CharField(max_length=500, blank=True, help_text="Google Maps embed URL (optional)")

    class Meta:
        verbose_name        = 'Company Profile'
        verbose_name_plural = 'Company Profile'

    def __str__(self):
        return 'Company Profile'
