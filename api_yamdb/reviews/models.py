from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Review(models.Model):
    title = models.IntegerField()
    text = models.TextField()
    author = models.IntegerField()
    score = models.IntegerField(
        validators=(MinValueValidator(1),MaxValueValidator(10)),
        error_messages={'validators': 'Оценка от 1 до 10.'}
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique review',
            ),
        )
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    author = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date')

    def __str__(self):
        return self.text[:20]
