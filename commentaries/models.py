from django.db import models


class Commentary(models.Model):
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')


class SubComment(models.Model):
    commentary = models.ForeignKey(
        Commentary,
        on_delete=models.CASCADE,
        related_name='sub_comment'
    )
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
