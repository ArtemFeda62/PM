from django.db import models

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

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(args, kwargs)
        self.images = None

    def __str__(self):
        return f"{self.name} - {self.code}"

    class Meta:
        verbose_name_plural = "Аномалии"
        verbose_name = "Аномалия"

class EGO(models.Model):
    anomalies = models.ForeignKey(Anomalies, on_delete=models.CASCADE, related_name='ego_gifts')
    name = models.CharField(max_length=100)
    slot = models.CharField(max_length=10)
    effect = models.TextField()

    def __str__(self):
        return f"{self.name} {self.slot}"

    class Meta:
        verbose_name_plural = "Дары EGO"
        verbose_name = "Дар EGO"

class MediaFiles(models.Model):
    anomalies = models.ForeignKey(Anomalies, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='anomalies_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Картинки аномалий"
        verbose_name = "Картинка аномалии"