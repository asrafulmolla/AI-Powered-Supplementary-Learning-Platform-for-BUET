import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from courses.models import Topic, CourseMaterial
from django.utils import timezone

def populate():
    # clear existing data
    CourseMaterial.objects.all().delete()
    Topic.objects.all().delete()

    # Create Topics
    t_ds = Topic.objects.create(name="Data Structures", description="Fundamental data structures")
    t_algo = Topic.objects.create(name="Algorithms", description="Algorithm design and analysis")
    t_db = Topic.objects.create(name="Database Systems", description="Relational databases and SQL")
    t_os = Topic.objects.create(name="Operating Systems", description="OS concepts, concurrency, and visualization")
    t_ai = Topic.objects.create(name="Artificial Intelligence", description="Search, ML, and Neural Networks")

    print(f"Created Topics: {t_ds}, {t_algo}, {t_db}, {t_os}, {t_ai}")

    # Create Theory Materials
    m1 = CourseMaterial.objects.create(
        title="Introduction to Arrays and Linked Lists",
        description="Basic concepts of linear data structures.",
        category="THEORY",
        file_type="SLIDE",
        topic=t_ds,
        week=1,
        tags="arrays, linked lists, linear",
        text_content="Arrays are contiguous memory blocks. Linked lists are node-based structures."
    )

    m2 = CourseMaterial.objects.create(
        title="Sorting Algorithms",
        description="Detailed analysis of QuickSort and MergeSort.",
        category="THEORY",
        file_type="PDF",
        topic=t_algo,
        week=3,
        tags="sorting, quicksort, mergesort",
        text_content="QuickSort is O(n log n) on average. MergeSort is stable."
    )

    m3 = CourseMaterial.objects.create(
        title="Normalization in DBMS",
        description="Understanding 1NF, 2NF, 3NF and BCNF.",
        category="THEORY",
        file_type="NOTE",
        topic=t_db,
        week=4,
        tags="normalization, sql, database",
        text_content="Normalization reduces redundancy. 3NF removes transitive dependencies."
    )

    CourseMaterial.objects.create(
        title="Process Synchronization & Deadlocks",
        description="Mutex, Semaphores and Deadlock conditions",
        category="THEORY",
        file_type="SLIDE",
        topic=t_os,
        week=6,
        tags="os, deadlock, semaphore, mutex",
        text_content="Deadlock requires mutual exclusion, hold and wait, no preemption, and circular wait. Semaphores are signaling mechanisms."
    )

    CourseMaterial.objects.create(
        title="Intro to Neural Networks",
        description="Perceptrons, Backpropagation and Activation Functions",
        category="THEORY",
        file_type="PDF",
        topic=t_ai,
        week=9,
        tags="ai, neural network, ml, deep learning",
        text_content="A perceptron is a binary classifier. Backpropagation is used to train neural networks using gradient descent."
    )

    # Create Lab Materials
    m4 = CourseMaterial.objects.create(
        title="Lab 01: Implementing Linked List",
        description="C++ implementation of a singly linked list.",
        category="LAB",
        file_type="CODE",
        topic=t_ds,
        week=1,
        tags="cpp, lab, pointers",
        text_content="struct Node { int data; Node* next; };"
    )

    m5 = CourseMaterial.objects.create(
        title="Lab 03: SQL Queries Practice",
        description="Practice basic SELECT, JOIN and GROUP BY queries.",
        category="LAB",
        file_type="OTHER",
        topic=t_db,
        week=4,
        tags="sql, lab, queries",
        text_content="SELECT * FROM students WHERE cgpa > 3.5;"
    )
    
    m6 = CourseMaterial.objects.create(
        title="Graph Traversal (BFS/DFS)",
        description="Implementation of BFS and DFS in Python",
        category="LAB",
        file_type="CODE",
        topic=t_algo,
        week=5,
        tags="graph, bfs, dfs, python",
        text_content="def bfs(graph, start): queue = [start] ..."
    )

    CourseMaterial.objects.create(
        title="Lab 05: Producer-Consumer Problem",
        description="Solving producer-consumer with pthreads in C",
        category="LAB",
        file_type="CODE",
        topic=t_os,
        week=7,
        tags="c, os, threads, concurrency",
        text_content="pthread_mutex_lock(&mutex); ... pthread_cond_wait(&cond, &mutex);"
    )

    print("Created 6 Course Materials.")

    # Create Community Posts
    from community.models import Post, Comment
    from community.bot_service import BotService

    # Clear existing community data
    Comment.objects.all().delete()
    Post.objects.all().delete()

    # Post 1: Normal discussion
    p1 = Post.objects.create(
        title="When is the deadline for Lab 03?",
        content="I am a bit confused about the submission date. Is it next Tuesday?",
        author_name="Student A"
    )
    Comment.objects.create(post=p1, author_name="Student B", content="Yes, it is next Tuesday at 11:59 PM.")

    # Post 2: Question triggering Bot
    p2 = Post.objects.create(
        title="Can someone explain Deadlocks?",
        content="I didn't fully understand the 4 necessary conditions for deadlock from the last lecture.",
        author_name="Student C"
    )
    # Manually trigger bot for populate script
    reply = BotService.generate_reply(p2.content)
    Comment.objects.create(post=p2, author_name="EduBot", content=reply, is_bot=True)
    p2.has_bot_reply = True
    p2.save()

    # Post 3: General discussion
    p3 = Post.objects.create(
        title="Group partners for Project",
        content="Looking for a partner for the final project. Must know Django.",
        author_name="Student D"
    )
    Comment.objects.create(post=p3, author_name="Student E", content="I am interested! Let's connect.")

    print(f"Created {Post.objects.count()} Community Posts.")

if __name__ == '__main__':
    populate()
