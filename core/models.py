from django.db import models


class Request(models.Model):
    method = models.CharField(max_length=16, verbose_name='Request Method')
    datetime = models.DateTimeField()
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.method} request at {self.datetime}"
    
    # set the date field to the date of the datetime field
    def save(self, *args, **kwargs):
        self.date = self.datetime.date()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date']

        verbose_name = 'Request'
        verbose_name_plural = 'Requests'
        
        indexes = [
            models.Index(fields=['date']),
        ]


class RequestSummary(models.Model):
    date = models.DateField()
    count = models.IntegerField()

    def __str__(self):
        return f"{self.date} - {self.count}"

    class Meta:
        verbose_name = 'Request Summary'
        verbose_name_plural = 'Requests Summary'
        # index date
        indexes = [
            models.Index(fields=['date']),
        ]