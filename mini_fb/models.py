from django.db import models
from django.urls import reverse


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    profile_pic = models.CharField(max_length=255, blank=True, null=True) 

    def get_status_messages(self):
        # Use the 'related_name' from the StatusMessage model (status_messages)
        return self.status_messages.all().order_by('-timestamp')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self):
        #Handles case where user is friends but also where user is the second node of the relation 
        friends_as_profile1 = Friend.objects.filter(profile1=self)
        friends_as_profile2 = Friend.objects.filter(profile2=self)
        
        friends_profiles = [friend.profile2 for friend in friends_as_profile1]
        friends_profiles += [friend.profile1 for friend in friends_as_profile2]

        return list(set(friends_profiles))
    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=280)  # Add max_length
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        return f"{self.profile.first_name}'s Message: {self.message[:50]}"  
    
    def get_images(self):
        return Image.objects.filter(status_message = self)


class Image(models.Model):
    image_file = models.ImageField(blank=True)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name="images")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now_add = True )

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"
    
    
    
