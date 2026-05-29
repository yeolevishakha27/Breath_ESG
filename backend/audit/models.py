from django.db import models

class AuditLog(models.Model):

    action = models.CharField(max_length=100)

    record_id = models.IntegerField()

    details = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.action