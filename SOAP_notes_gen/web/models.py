from django.db import models

class SOAPNote(models.Model):
    subjective = models.TextField()
    objective = models.TextField()
    assessment = models.TextField()
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
