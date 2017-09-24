from django.db import models

# Create your models here.
class Attendance(models.Model):
    user_id = models.BigIntegerField(null=False, blank=False)
    event_id = models.BigIntegerField(null=False, blank=False)
    status = models.PositiveSmallIntegerField(null=False, blank=False)

    class Meta:
        unique_together = ('user_id', 'event_id')

    def __str__(self):
        return  'user_id: {0}, event_id: {1}, status: {2}'.format(self.user_id, self.event_id, self.status)
