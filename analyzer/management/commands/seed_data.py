from django.core.management.base import BaseCommand
from analyzer.models import Category, Tag, TextDocument
from django.utils import timezone
import random


class Command(BaseCommand):
    help = "Seeds the database with initial data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        # Create Categories
        categories = ["Science", "Fiction", "News", "Technology", "History"]
        cat_objs = []
        for name in categories:
            cat, created = Category.objects.get_or_create(
                name=name, defaults={"description": f"Texts related to {name}"}
            )
            cat_objs.append(cat)

        # Create Tags
        tags = ["Easy", "Hard", "Long", "Short", "Review", "Analysis", "Essay"]
        tag_objs = []
        for name in tags:
            tag, created = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag)

        # Create Documents
        sample_texts = [
            (
                "The Theory of Relativity",
                "E = mc^2 is a famous equation derived by Albert Einstein. It relates energy to mass.",
                "Science",
            ),
            (
                "A Journey to the Center of the Earth",
                "The professor and his nephew climbed down the volcano. It was dark and scary.",
                "Fiction",
            ),
            (
                "Tech Trends 2026",
                "AI is evolving rapidly. Python remains the dominant language for data science.",
                "Technology",
            ),
            (
                "Daily News Update",
                "The weather today represents a significant shift from yesterday's patterns.",
                "News",
            ),
            (
                "The Roman Empire",
                "Julius Caesar was a prominent figure in Roman history. He crossed the Rubicon.",
                "History",
            ),
            (
                "Quantum Physics Basics",
                "Particles can exist in multiple states at once. This is called superposition.",
                "Science",
            ),
            (
                "The Martian",
                "Mark Watney was stranded on Mars. He had to grow potatoes to survive.",
                "Fiction",
            ),
            (
                "New Gadgets Release",
                "The latest smartphone features a holographic display and infinite battery life.",
                "Technology",
            ),
            (
                "Global Economics",
                "Inflation rates have stabilized across major markets. Trade agreements are being signed.",
                "News",
            ),
            (
                "Ancient Egypt",
                "The pyramids were built as tombs for pharaohs. Mummification was a complex process.",
                "History",
            ),
        ]

        for title, content, cat_name in sample_texts:
            category = Category.objects.get(name=cat_name)
            doc, created = TextDocument.objects.get_or_create(
                title=title, defaults={"content": content, "category": category}
            )
            if created:
                # Add 1-3 random tags
                doc_tags = random.sample(tag_objs, k=random.randint(1, 3))
                doc.tags.set(doc_tags)
                self.stdout.write(f"Created document: {title}")
            else:
                self.stdout.write(f"Document exists: {title}")

        self.stdout.write(self.style.SUCCESS("Successfully seeded database"))
