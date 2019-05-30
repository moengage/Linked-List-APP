from rest_framework.views import APIView
from django.db.models import F

from .serializers import NodeSerializer, LinkedListSerializer
from .models import Node, LinkedList
from rest_framework import status
from rest_framework.response import Response
from .utils import find_node_data, pop_data, remove_node, reverse_linked_list


class LinkedListAPI(APIView):
    model = Node

    def post(self, request):
        """
        Create a node , As post request will be done only when creating a linked list,
        I have hardcoded the length
        """
        serializer = NodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        LinkedList.objects.create(start_node=instance, length=1)
        data = serializer.data
        data["id"] = instance.id
        data["next"] = instance.next_node
        response = {
            "meta" : {
                    "id" : instance.linkedlist_set.all().first().id,
                    "length" : instance.linkedlist_set.all().first().length
                    },
            "object" : [
                data
            ]

        }
        return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request, unique_id):
        """
        Getting details of linked list
        """
        if not unique_id:
            return Response("Missing Data", status=status.HTTP_400_BAD_REQUEST)

        instance = LinkedList.objects.filter(id=unique_id)

        if not instance:
            return Response("Wrong id", status=status.HTTP_400_BAD_REQUEST)

        instance = instance[0]

        head_node = Node.objects.get(id=instance.start_node.id)
        object = find_node_data(head_node)

        response = {
            "meta": {
                "id": instance.id,
                "length": instance.length
            },
            "object": object
        }

        return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, unique_id):
        if not unique_id:
            return Response("Missing Data", status=status.HTTP_400_BAD_REQUEST)

        instance_list = LinkedList.objects.filter(id=unique_id)

        if not instance_list:
            return Response("Wrong id", status=status.HTTP_400_BAD_REQUEST)

        instance_list = instance_list[0]

        data = request.data
        serializer = NodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        start = Node.objects.get(id=instance_list.start_node.id)
        head_node = start

        while start.next_node != None:
            start = start.next_node

        start.next_node = instance
        start.save()
        instance_list.length += 1
        instance_list.save()

        object = find_node_data(head_node)

        response = {
            "meta": {
                "id": instance_list.id,
                "length": instance_list.length
            },
            "object": object
        }

        return Response(response, status=status.HTTP_201_CREATED)

    def delete(self, request, unique_id):
        if not unique_id:
            return Response("Missing Data", status=status.HTTP_400_BAD_REQUEST)

        instance = LinkedList.objects.filter(id=unique_id)

        if not instance:
            return Response("No such Linked List Exists", status=status.HTTP_400_BAD_REQUEST)

        instance = instance[0]
        LinkedList.objects.filter(id=unique_id).delete()

        return Response([], status=status.HTTP_204_NO_CONTENT)


class LinkedListPopAPI(APIView):

    def get(self, request, unique_id):
        """
        Pop last element from linked list
        """

        if not unique_id:
            return Response("Missing Data", status=status.HTTP_400_BAD_REQUEST)

        instance = LinkedList.objects.filter(id=unique_id)

        if not instance:
            return Response("Wrong id", status=status.HTTP_400_BAD_REQUEST)

        instance = instance[0]

        head_node = Node.objects.get(id=instance.start_node.id)
        object = pop_data(head_node)

        if len(object) ==0:
            return Response([], status=status.HTTP_201_CREATED)

        LinkedList.objects.filter(id=unique_id).update(length=F('length')-1)
        instance = LinkedList.objects.filter(id=unique_id)

        instance = instance[0]

        response = {
            "meta": {
                "id": instance.id,
                "length": instance.length
            },
            "object": object
        }

        return Response(response, status=status.HTTP_201_CREATED)

    def post(self, request, unique_id):
        """
        Remove any element from linked list.
        Two case to handle :
        1) Object does not exists
        2) Object exists - is head node , is not head node
        """
        if not unique_id:
            return Response("Missing Data", status=status.HTTP_400_BAD_REQUEST)

        instance = LinkedList.objects.filter(id=unique_id)
        data = request.data
        if not instance or 'name' not in data or 'birthyear' not in data:
            return Response("Wrong id", status=status.HTTP_400_BAD_REQUEST)

        instance = instance[0]

        head_node = Node.objects.get(id=instance.start_node.id)

        flag=0

        object = remove_node(head_node, data)

        if object==-1:
            return Response("No such node exists in Linked list", status=status.HTTP_400_BAD_REQUEST)
        elif len(object)==0:
            return Response("Whole Linked List is deleted", status=status.HTTP_200_OK)
        else:
            instance = LinkedList.objects.filter(id=unique_id)

            instance = instance[0]

            response = {
                "meta": {
                    "id": instance.id,
                    "length": instance.length
                },
                "object": object
            }

            return Response(response, status=status.HTTP_200_OK)



class ReverseLinkedList(APIView):
    """
    Reverse Linked List
    """

    def get(self, request, unique_id):
        if not unique_id:
            return Response("Missing Data", status=status.HTTP_400_BAD_REQUEST)

        instance = LinkedList.objects.filter(id=unique_id)

        if not instance:
            return Response("Wrong id", status=status.HTTP_400_BAD_REQUEST)

        instance = instance[0]

        head_node = Node.objects.get(id=instance.start_node.id)
        object = reverse_linked_list(head_node)

        instance = LinkedList.objects.filter(id=unique_id)
        instance = instance[0]

        response = {
            "meta": {
                "id": instance.id,
                "length": instance.length
            },
            "object": object
        }

        return Response(response, status=status.HTTP_200_OK)




