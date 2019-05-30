from app.models import Node, LinkedList
import copy


def find_node_data(head_node):
    lis = []

    while head_node.next_node!= None:
        temp = {
            "id" : head_node.id,
            "name" : head_node.name,
            "birthyear" : head_node.birthyear,
            "next" : head_node.next_node.id
        }
        lis.append(temp)
        head_node = head_node.next_node

    temp = {
        "id": head_node.id,
        "name": head_node.name,
        "birthyear": head_node.birthyear,
        "next": head_node.next_node
    }
    lis.append(temp)

    return lis


def pop_data(head_node):
    lis = []
    prev = head_node
    root = head_node

    while root.next_node != None:
        temp = {
            "id": root.id,
            "name": root.name,
            "birthyear": root.birthyear,
            "next": root.next_node.id
        }
        prev = root
        root = root.next_node
        if root.next_node == None:
            temp["next"] = None
        lis.append(temp)

    #Delete first node
    if len(lis)==0:
        Node.objects.filter(id=prev.id).delete()
        return lis

    prev.next_node = None
    prev.save()

    return lis


def remove_node(head_node, data_to_remove):
    """
    Two case to handle :
        1) Object does not exists
        2) Object exists - is head node , is not head node
    """
    flag = 0
    head = copy.deepcopy(head_node)
    #When node to be removed is head
    if head_node.birthyear == data_to_remove['birthyear'] and head_node.name ==data_to_remove['name']:

        if head_node.next_node == None:
            linked = LinkedList.objects.filter(start_node=head_node.id).delete()
            return []

        next = copy.deepcopy(head_node.next_node)
        head = next
        head_node.next_node = None
        head_node.save()
        id = LinkedList.objects.filter(start_node=head_node)[0].id
        LinkedList.objects.filter(start_node=head_node).delete()
        LinkedList.objects.create(start_node=next, id=id)

    else:

        prev = head_node
        root = head_node

        while root.next_node != None:
            if root.name == data_to_remove['name'] and root.birthyear == data_to_remove['birthyear']:
                flag = 1
                break
            prev = root
            root = root.next_node

        if root.name == data_to_remove['name'] and root.birthyear == data_to_remove['birthyear']:
            flag = 1

        #When node to be deleted is not found
        if flag ==0:
            return -1

        prev.next_node = prev.next_node.next_node
        prev.save()

    lis = []
    root = head

    while root.next_node != None:
        if root.name == data_to_remove['name'] and root.birthyear == data_to_remove['birthyear']:
            root = root.next_node
            continue
        temp = {
            "id": root.id,
            "name": root.name,
            "birthyear": root.birthyear,
            "next": root.next_node.id
        }
        root = root.next_node
        lis.append(temp)
    temp = {
        "id": root.id,
        "name": root.name,
        "birthyear": root.birthyear,
        "next": None
    }
    lis.append(temp)
    return lis


def reverse_linked_list(head_node):
    """
    Two cases arises:
    1) We get linked list of single node
    2) We get linked list of more than 2 nodes.
    """
    lis = []
    if head_node.next_node==None:
        temp = {
            "id": head_node.id,
            "name": head_node.name,
            "birthyear": head_node.birthyear,
            "next": None
        }
        lis.append(temp)
        return lis
    else:
        prev = None
        root = head_node
        next = None
        id = LinkedList.objects.get(start_node=head_node).id
        length = LinkedList.objects.get(start_node=head_node).length
        LinkedList.objects.filter(start_node=head_node).delete()
        while root != None:
            next = copy.deepcopy(root.next_node)
            root.next_node = prev
            prev = copy.deepcopy(root)
            root = next
            prev.save()
        prev.save()
        LinkedList.objects.create(start_node=prev, id=id, length=length)

        while prev.next_node!=None:
            temp = {
                "id": prev.id,
                "name": prev.name,
                "birthyear": prev.birthyear,
                "next": prev.next_node.id
            }
            prev = prev.next_node
            lis.append(temp)

        temp = {
            "id": prev.id,
            "name": prev.name,
            "birthyear": prev.birthyear,
            "next": None
        }
        lis.append(temp)
        return lis






