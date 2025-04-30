class Character:
    def __init__(self, name, age, gender, occupation, personality, backstory, physical_traits, motivations, relationships=None):
        self.name = name
        self.age = age
        self.gender = gender
        self.occupation = occupation
        self.personality = personality
        self.backstory = backstory
        self.physical_traits = physical_traits
        self.motivations = motivations
        self.relationships = relationships or {}  # Dictionary: {character_name: relationship_type}
        self.development = []  # Tracks character growth

    def get_summary(self):
        rel_str = "\n".join([f"  - {char}: {rel}" for char, rel in self.relationships.items()]) if self.relationships else "None"
        dev_str = "\n".join(self.development) if self.development else "No development yet."
        return f"""
Name: {self.name}
Age: {self.age}
Gender: {self.gender}
Occupation: {self.occupation}
Personality: {self.personality}
Backstory: {self.backstory}
Physical Traits: {self.physical_traits}
Motivations: {self.motivations}
Relationships:
{rel_str}
Development:
{dev_str}
"""

    def add_development(self, chapter_num, event):
        self.development.append(f"Chapter {chapter_num}: {event}")