from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):
    # You can add additional fields here if needed
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='images/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    

    @property
    def age(self):
        if self.birth_date:
            from datetime import date
            today = date.today()
            age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
            if today.month == self.birth_date.month and today.day == self.birth_date.day:
                age_store = {
                    'message': "{} is {} years old. 🎉 Happy Birthday!".format(self.get_full_name(), age)

                }
                return age_store
            else:
                return age
            
        return None
    def __str__(self):
        return self.username + " "+ self.email
    @property
    def is_premium(self):
        if hasattr(self, 'premium_profile'):
            return self.premium_profile.is_active_premim()
        return False
    


class PremiumUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='premium_profile')
    membrership_start_date = models.DateField(
        default = models.functions.Now(),
        help_text="The date when the user started their premium membership."
    )
    membership_end_date = models.DateField(
        blank=True
    )
    premium_features_enabled = models.BooleanField(
        default=True,
        help_text="Indicates Whether the premium features are enabled for the user."
    )


    class Meta:
        verbose_name = "Premium User"
        verbose_name_plural = "Premium Users"
    def __str__(self):
        return f"{self.user.email} - Premium user"

    def is_active_premim(self):
        from datetime import date
        if self.premium_features_enabled:
            today = date.today()
            if self.membership_start_date <= today:
                if self.membership_end_date >= today:
                    return True    
                
        return False
            
    
    
        


 