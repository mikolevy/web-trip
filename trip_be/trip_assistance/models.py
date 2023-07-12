from django.db import models


class BusLine(models.Model):
    number = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"Bus Line - Number: {self.number}"
