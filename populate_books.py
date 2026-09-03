import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from catalog.models import Book

books_data = [
    {"title": "Clean Code", "author": "Robert C. Martin", "category": "Software Engineering", "isbn": "978-0132350884", "key": "clean_code"},
    {"title": "Clean Architecture", "author": "Robert C. Martin", "category": "Software Engineering", "isbn": "978-0134494166", "key": "Clean_Architecture"},
    {"title": "Computer Networking: A Top-Down Approach", "author": "James Kurose", "category": "Networking", "isbn": "978-0133594140", "key": "Computer_Networking"},
    {"title": "Data Structures and Algorithms", "author": "Mark Allen Weiss", "category": "Computer Science", "isbn": "978-0132847377", "key": "data_structure"},
    {"title": "Introduction to Networking", "author": "Cisco Academy", "category": "Networking", "isbn": "978-1587133602", "key": "introduction_to_network"},
    {"title": "Operating System Concepts", "author": "Abraham Silberschatz", "category": "Operating Systems", "isbn": "978-1118063330", "key": "Operating_System"},
    {"title": "Python Crash Course", "author": "Eric Matthes", "category": "Programming", "isbn": "978-1593279288", "key": "python_crash_course"},
]

covers_dir = os.path.join('media', 'covers')
files_in_covers = os.listdir(covers_dir) if os.path.exists(covers_dir) else []

for item in books_data:
    matched_file = None
    for f in files_in_covers:
        if item["key"].lower() in f.lower():
            matched_file = f"covers/{f}"
            break

    book, created = Book.objects.get_or_create(
        title=item["title"],
        defaults={
            "author": item["author"],
            "category": item["category"],
            "isbn": item["isbn"],
            "total_copies": 5,
            "available_copies": 5,
            "cover": matched_file
        }
    )
    if created:
        print(f"✅ تم إضافة: {item['title']}")
    else:
        print(f"ℹ️ موجود بالفعل: {item['title']}")

print("\nتمت إضافة جميع الكتب بنجاح!")