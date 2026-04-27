from django.db import models
from typing import Any

class Anomalies(models.Model):
    Risk_levels = [
        ('ZAYIN', 'ZAYIN'),
        ('TETH', 'TETH'),
        ('HE', 'HE'),
        ('WAW', 'WAW'),
        ('ALEPH', 'ALEPH'),
    ]
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    risk_level = models.CharField(max_length=10, choices=Risk_levels)
    description = models.TextField()
    removed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.code}"

    class Meta:
        verbose_name = "Аномалия"
        verbose_name_plural = "Аномалии"

class EGO(models.Model):
    anomaly = models.ForeignKey(Anomalies, on_delete=models.CASCADE, related_name='ego_gifts')
    name = models.CharField(max_length=100)
    slot = models.CharField(max_length=10)
    effect = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.slot})"

    class Meta:
        verbose_name = "Дар EGO"
        verbose_name_plural = "Дары EGO"

class MediaFiles(models.Model):
    anomaly = models.ForeignKey(Anomalies, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='anomalies_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Изображение аномалии"
        verbose_name_plural = "Изображения аномалий"