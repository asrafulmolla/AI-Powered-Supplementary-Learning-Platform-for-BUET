import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from courses.models import Topic, CourseMaterial

def seed():
    # Topics
    t1, _ = Topic.objects.get_or_create(name="Data Structures", description="Fundamental data structures like arrays, lists, trees, and graphs.")
    t2, _ = Topic.objects.get_or_create(name="Algorithms", description="Sorting, searching, and dynamic programming.")
    t3, _ = Topic.objects.get_or_create(name="Networking", description="OSI layers, protocols, and routing.")

    # Materials
    CourseMaterial.objects.get_or_create(
        title="Introduction to Linked Lists",
        description="A comprehensive guide to singly and doubly linked lists.",
        topic=t1,
        category="Theory",
        file_type="PDF",
        text_content="# Linked Lists\n\nLinked lists are linear data structures where elements are stored in nodes. Each node contains data and a pointer to the next node.\n\n## Types\n1. Singly Linked List\n2. Doubly Linked List\n3. Circular Linked List\n\n$$\text{Next} = \text{Node} \to \text{next}$$",
        week=1,
        tags="ds, pointers"
    )

    CourseMaterial.objects.get_or_create(
        title="QuickSort Implementation",
        description="Efficient sorting using divide and conquer.",
        topic=t2,
        category="Lab",
        file_type="CODE",
        text_content="def quicksort(arr):\n    if len(arr) <= 1: return arr\n    pivot = arr[len(arr)//2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)",
        week=2,
        tags="sorting, recursion"
    )

    print("Database seeded successfully with core materials.")

if __name__ == "__main__":
    seed()
