from django.urls import reverse
from User_Profile.models import *


class Work(models.Model):
    name_work = models.CharField(max_length=200)
    description_work = models.TextField()
    date_work = models.DateTimeField(default=timezone.now)

    done_work = models.BooleanField(default=False)
    Paid_work = models.BooleanField(default=False)

    client_work = models.OneToOneField(ClientProfile, on_delete=models.CASCADE)
    assigned_work = models.OneToOneField(WorkerProfile, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse('work-detail', kwargs={'pk': self.pk})
