from django.core.management.base import BaseCommand
from analyzer.models import Category, Tag, TextDocument
from django.utils import timezone
import random


class Command(BaseCommand):
    help = "Seeds the database with initial data (Long Texts)"

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        # Create Categories
        categories = ["Science", "Literature", "History", "Technology", "Philosophy"]
        cat_objs = []
        for name in categories:
            cat, created = Category.objects.get_or_create(
                name=name, defaults={"description": f"Texts related to {name}"}
            )
            cat_objs.append(cat)

        # Create Tags
        tags = ["Educational", "Complex", "Long Read", "Technical", "Biography", "Nature", "Abstract"]
        tag_objs = []
        for name in tags:
            tag, created = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag)

        # Long Sample Texts
        long_science_text = """
Quantum mechanics is a fundamental theory in physics that provides a description of the physical properties of nature at the scale of atoms and subatomic particles. It is the foundation of all quantum physics including quantum chemistry, quantum field theory, quantum technology, and quantum information science.
Classical physics, the collection of theories that existed before the advent of quantum mechanics, describes many aspects of nature at an ordinary (macroscopic) scale, but is not sufficient for describing them at small (atomic and subatomic) scales. Most theories in classical physics can be derived from quantum mechanics as an approximation valid at large (macroscopic) scale.
Flux quantization, the property that the magnetic flux in a superconducting loop involves the magnetic flux quantum, was discovered in 1961 by Deaver and Fairbank and, independently, by Doll and Näbauer. The quantization of magnetic flux in a superconductor is a consequence of the requirement that the wave function be single-valued.
Energy systems in quantum mechanics can be continuous or discrete. In discrete systems, there are a countable number of states, and in continuous systems, there are an uncountable number of states.
        """

        long_history_text = """
The Industrial Revolution was the transition to new manufacturing processes in Great Britain, continental Europe, and the United States, in the period from about 1760 to sometime between 1820 and 1840. This transition included going from hand production methods to machines, new chemical manufacturing and iron production processes, the increasing use of steam power and water power, the development of machine tools and the rise of the mechanized factory system. The Industrial Revolution also led to an unprecedented rise in the rate of population growth.
Textiles were the dominant industry of the Industrial Revolution in terms of employment, value of output and capital invested. The textile industry was also the first to use modern production methods.
The Industrial Revolution began in Great Britain, and many of the technological innovations were of British origin. By the mid-18th century Britain was the world's leading commercial nation, controlling a global trading empire with colonies in North America and the Caribbean, and with major political influence on the Indian subcontinent, through the activities of the East India Company.
The transition to industrialization was not without its challenges. It brought about significant social and economic changes, including urbanization, the rise of the factory system, and changes in labor conditions.
        """

        long_tech_text = """
Artificial intelligence (AI) is intelligence associated with computational devices. It is a field of research in computer science and engineering. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.
The term "artificial intelligence" was used to describe machines that mimic and display "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving". This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.
AI applications include advanced web search engines (e.g., Google), recommendation systems (used by YouTube, Amazon and Netflix), understanding human speech (such as Siri and Alexa), self-driving cars (e.g., Waymo), generative or creative tools (ChatGPT and AI art), automated decision-making and competing at the highest level in strategic game systems (such as chess and Go).
As AI technology continues to evolve, it raises important ethical and societal questions regarding privacy, bias, and the future of work.
        """

        long_literature_text = """
The Great Gatsby is a 1925 novel by American writer F. Scott Fitzgerald. Set in the Jazz Age on Long Island, near New York City, the novel depicts first-person narrator Nick Carraway's interactions with mysterious millionaire Jay Gatsby and Gatsby's obsession to reunite with his former lover, Daisy Buchanan.
The novel was inspired by a youthful romance Fitzgerald had with a socialite, and by parties he attended on Long Island's North Shore in 1922. Following a move to the French Riviera, he drafted the novel in 1924. Its editor, Maxwell Perkins, persuaded Fitzgerald to make revisions during the following winter. After his revisions, Fitzgerald was satisfied with the text, but remained ambivalent about the book's title and considered several alternatives. The Great Gatsby was first published by Scribner's in April 1925.
Upon its release, The Great Gatsby received mixed reviews from literary critics, who considered its content significantly different from Fitzgerald's previous efforts. It sold poorly compared to his earlier novels: 20,000 copies of the first edition were printed, but not all were sold. Fitzgerald died in 1940, believing himself to be a failure and his work forgotten. However, during World War II, the novel faced a critical and commercial re-examination, and it soon became a core part of the American high school curriculum.
Today, The Great Gatsby is widely considered a literary masterpiece and a contender for the title of the Great American Novel.
        """

        # Create Documents
        sample_texts = [
            ("Quantum Physics Explained", long_science_text, "Science"),
            ("The Industrial Revolution", long_history_text, "History"),
            ("Artificial Intelligence Overview", long_tech_text, "Technology"),
            ("The Great Gatsby Summary", long_literature_text, "Literature"),
            (
                "Short Stoicism Intro",
                "Stoicism is a school of Hellenistic philosophy founded by Zeno of Citium in Athens in the early 3rd century BC. It is a philosophy of personal ethics informed by its system of logic and its views on the natural world.",
                "Philosophy"
            ),
             (
                "Python Programming",
                "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a 'batteries included' language due to its comprehensive standard library.",
                "Technology"
            ),
        ]

        for title, content, cat_name in sample_texts:
             # Find or create category if it was missed in loop
            category, _ = Category.objects.get_or_create(name=cat_name)
            
            doc, created = TextDocument.objects.get_or_create(
                title=title,
                defaults={
                    "content": content.strip(),
                    "category": category,
                    "created_at": timezone.now()
                }
            )
            
            if created:
                # Assign random tags
                num_tags = min(len(tag_objs), random.randint(2, 4))
                doc_tags = random.sample(tag_objs, k=num_tags)
                doc.tags.set(doc_tags)
                self.stdout.write(self.style.SUCCESS(f"Created document: {title} ({len(content)} chars)"))
            else:
                self.stdout.write(self.style.WARNING(f"Document already exists: {title}"))

        self.stdout.write(self.style.SUCCESS("Seeding completed!"))
