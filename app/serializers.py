from .models import Node, LinkedList
from rest_framework import serializers


class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        fields = ["name", "birthyear"]


class LinkedListSerializer(serializers.ModelSerializer):

    class Meta:
        model = LinkedList
        fields = ["start_node", "length"]

