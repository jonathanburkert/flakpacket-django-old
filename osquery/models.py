from django.db import models

class enrolled_nodes(models.Model):

    address = models.CharField(max_length=50)
    node_key = models.CharField(max_length=50)

    def __str__(self):
        return self.address


class alerts(models.Model):

    src_ip = models.CharField(max_length=50)
    src_port = models.CharField(max_length=50)
    dest_ip = models.CharField(max_length=50)
    dest_port = models.CharField(max_length=50)
    uid = models.CharField(max_length=50)

    def __str__(self):
        return "{}:{} => {}:{}".format(self.src_ip, self.src_port, self.dest_ip, self.dest_port)
