from django.db import models


class Node(models.Model):
    name = models.CharField(max_length=200)
    birthyear = models.IntegerField(default=1996)
    next_node = models.ForeignKey("self", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class LinkedList(models.Model):
    start_node = models.ForeignKey(Node, on_delete=models.CASCADE)
    length = models.IntegerField(default=1)


