from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Category, Course

# category -> [(title, instructor, price), ...]
DATA = {
    "Backend Development": [
        ("Python for Backend Developers", "Adaeze Okafor", 25000),
        ("Django REST Framework Masterclass", "Tunde Bakare", 35000),
        ("Building APIs with FastAPI", "Chiamaka Eze", 30000),
        ("Node.js and Express Fundamentals", "Ibrahim Musa", 28000),
        ("Authentication and Security for APIs", "Funke Adeyemi", 32000),
    ],
    "Frontend Development": [
        ("HTML and CSS from Scratch", "Kemi Balogun", 15000),
        ("Modern JavaScript (ES6+)", "Samuel Nwosu", 22000),
        ("React for Beginners", "Zainab Yusuf", 30000),
        ("Responsive Design with Tailwind CSS", "David Okoro", 18000),
        ("TypeScript Essentials", "Grace Adebayo", 26000),
    ],
    "Data Science": [
        ("Data Analysis with Pandas", "Emeka Obi", 27000),
        ("SQL for Data Analysts", "Halima Sani", 20000),
        ("Data Visualization with Matplotlib", "Tolu Ajayi", 24000),
        ("Statistics for Data Science", "Peter Umeh", 29000),
        ("Intro to Machine Learning", "Ngozi Anene", 40000),
    ],
    "Cloud and DevOps": [
        ("Docker for Developers", "Yusuf Lawal", 28000),
        ("Git and GitHub Workflows", "Blessing Ojo", 12000),
        ("CI/CD with GitHub Actions", "Chinedu Eze", 30000),
        ("AWS Cloud Practitioner Prep", "Amina Garba", 38000),
        ("Linux Command Line Essentials", "Femi Adewale", 16000),
    ],
    "Cybersecurity": [
        ("Cybersecurity Fundamentals", "Ola Johnson", 25000),
        ("Ethical Hacking for Beginners", "Musa Danjuma", 35000),
        ("Web Application Security (OWASP Top 10)", "Ifeoma Nnadi", 33000),
        ("Network Security Basics", "Seun Ogunleye", 27000),
        ("Secure Coding Practices", "Hauwa Abdullahi", 30000),
    ],
}


class Command(BaseCommand):
    help = "Seed the database with sample categories and courses."

    @transaction.atomic
    def handle(self, *args, **options):
        created_courses = 0
        for cat_name, courses in DATA.items():
            category, _ = Category.objects.get_or_create(name=cat_name)
            for title, instructor, price in courses:
                _, created = Course.objects.get_or_create(
                    title=title,
                    defaults={
                        "category": category,
                        "instructor": instructor,
                        "price": price,
                        "description": f"{title} taught by {instructor}.",
                    },
                )
                created_courses += created

        self.stdout.write(self.style.SUCCESS(
            f"Done. {Category.objects.count()} categories, "
            f"{created_courses} new courses created."
        ))