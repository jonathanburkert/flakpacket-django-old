from django.db import models

class enrolled_nodes(models.Model):

    address = models.CharField(max_length=50)
    node_key = models.CharField(max_length=50)

    def __str__(self):
        return self.address

