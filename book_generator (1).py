import random
import os
import sys
import platform
from datetime import datetime

def check_environment():
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Current Directory: {os.getcwd()}")
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)

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
        self.relationships = relationships or {}
        self.development = []

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

class BookGenerator:
    def __init__(self):
        self.characters = []
        self.genre = ""
        self.setting = ""
        self.tone = ""
        self.themes = []
        self.page_count = 100
        self.chapter_count = 10
        self.conflict_intensity = "medium"
        self.plot = ""
        self.title = ""
        self.key_plot_points = []

    def validate_non_empty_string(self, value, field_name):
        value = value.strip() if value else ""
        if not value:
            raise ValueError(f"{field_name} cannot be empty.")
        return value

    def validate_integer(self, value, field_name, min_val=None, max_val=None):
        try:
            num = int(value)
            if min_val is not None and num < min_val:
                raise ValueError(f"{field_name} must be at least {min_val}.")
            if max_val is not None and num > max_val:
                raise ValueError(f"{field_name} must be at most {max_val}.")
            return num
        except (ValueError, TypeError):
            raise ValueError(f"{field_name} must be a valid integer.")

    def add_character(self, name, age, gender, occupation, personality, backstory, physical_traits, motivations, relationships):
        try:
            age = self.validate_integer(age, "Age", min_val=0)
            name = self.validate_non_empty_string(name, "Name")
            character = Character(name, age, gender, occupation, personality, backstory, physical_traits, motivations, relationships)
            self.characters.append(character)
            return character.get_summary()
        except ValueError as e:
            return f"Error: {e}"

    def set_book_details(self, genre, setting, tone, themes, page_count, chapter_count, conflict_intensity, title, key_plot_points):
        try:
            self.genre = self.validate_non_empty_string(genre, "Genre")
            self.setting = self.validate_non_empty_string(setting, "Setting")
            self.tone = self.validate_non_empty_string(tone, "Tone")
            self.themes = [t.strip() for t in themes if t.strip()]
            if not self.themes:
                raise ValueError("At least one theme is required.")
            self.page_count = self.validate_integer(page_count, "Page Count", min_val=100, max_val=400)
            self.chapter_count = self.validate_integer(chapter_count, "Chapter Count", min_val=10, max_val=100)
            self.conflict_intensity = conflict_intensity.lower() if conflict_intensity else "medium"
            if self.conflict_intensity not in ["low", "medium", "high"]:
                raise ValueError("Conflict intensity must be low, medium, or high.")
            self.title = self.validate_non_empty_string(title, "Title")
            self.key_plot_points = key_plot_points
            return "Book details set successfully!"
        except ValueError as e:
            return f"Error: {e}"

    def generate_plot(self):
        if len(self.characters) < 2:
            return "Error: At least 2 characters are required to generate a plot."
        
        protagonist = self.characters[0]
        antagonist = self.characters[1] if len(self.characters) > 1 else None
        
        conflict_types = {
            "Fantasy": ["quest for a magical artifact", "battle against dark forces", "coming-of-age journey"],
            "Sci-Fi": ["intergalactic war", "AI rebellion", "colonization of new planet"],
            "Mystery": ["murder investigation", "missing person case", "conspiracy unraveling"],
            "Romance": ["forbidden love", "second-chance romance", "love triangle"],
            "Thriller": ["political conspiracy", "race against time", "serial killer pursuit"]
        }
        
        intensity_modifiers = {
            "low": "subtle, character-driven",
            "medium": "balanced, engaging",
            "high": "intense, action-packed"
        }
        
        conflict = random.choice(conflict_types.get(self.genre, ["personal struggle", "rivalry", "quest for truth"]))
        intensity_desc = intensity_modifiers.get(self.conflict_intensity, "balanced, engaging")
        
        rel_desc = ""
        if antagonist and antagonist.name in protagonist.relationships:
            rel_desc = f"Their {protagonist.relationships[antagonist.name].lower()} relationship fuels the tension. "
        
        plot_points_desc = ""
        if self.key_plot_points:
            plot_points_desc = f"Key events include {', '.join(self.key_plot_points).lower()}. "
        
        self.plot = f"""
In {self.setting}, {protagonist.name}, a {protagonist.occupation}, embarks on a {self.tone} journey driven by {protagonist.motivations.lower()}.
The story revolves around {intensity_desc} {conflict}. {antagonist.name if antagonist else 'An opposing force'}, motivated by {antagonist.motivations.lower() if antagonist else 'conflicting goals'}, creates obstacles.
{rel_desc}{plot_points_desc}Key themes include {', '.join(self.themes)}. The narrative unfolds through {protagonist.name}'s perspective, with {self.conflict_intensity} stakes shaped by {self.genre.lower()} elements.
"""
        return self.plot

    def preview_book_structure(self):
        if not self.plot or not self.characters or not self.genre:
            return "Error: Please add characters, set book details, and generate a plot first."
        
        pages_per_chapter = self.page_count // self.chapter_count
        preview = f"""
# {self.title} (Preview)

*Genre*: {self.genre}  
*Setting*: {self.setting}  
*Tone*: {self.tone}  
*Themes*: {', '.join(self.themes)}  
*Conflict Intensity*: {self.conflict_intensity}  
*Page Count*: {self.page_count}  
*Chapter Count*: {self.chapter_count}  
*Pages per Chapter*: ~{pages_per_chapter}  
*Key Plot Points*: {', '.join(self.key_plot_points) if self.key_plot_points else 'None'}

## Character Summaries
{''.join([c.get_summary() for c in self.characters])}

## Plot Summary
{self.plot}

## Chapter Outline
"""
        narrative_arc = ["Introduction", "Rising Action", "Climax", "Falling Action", "Resolution"]
        arc_length = self.chapter_count // len(narrative_arc)
        for i in range(1, self.chapter_count + 1):
            arc_index = min((i - 1) // arc_length, len(narrative_arc) - 1)
            arc_stage = narrative_arc[arc_index]
            event = random.choice(["confrontation", "discovery", "alliance", "revelation", "setback"])
            preview += f"Chapter {i} ({arc_stage}): A {self.conflict_intensity} {event} involving {random.choice([c.name for c in self.characters])}. (~{pages_per_chapter} pages)\n"
        
        return preview

    def generate_chapter(self, chapter_num, pages_per_chapter, arc_stage):
        characters_involved = random.sample(self.characters, min(len(self.characters), random.randint(2, 4)))
        character_names = [c.name for c in characters_involved]
        intensity_events = {
            "low": ["a quiet realization", "a subtle misunderstanding", "a heartfelt conversation"],
            "medium": ["a heated confrontation", "a critical discovery", "an unexpected alliance"],
            "high": ["a life-threatening chase", "a world-altering revelation", "a brutal betrayal"]
        }
        arc_events = {
            "Introduction": ["sets the stage", "introduces key tensions", "establishes motives"],
            "Rising Action": ["escalates conflict", "builds stakes", "deepens relationships"],
            "Climax": ["reaches peak tension", "forces a turning point", "reveals critical truths"],
            "Falling Action": ["resolves major conflicts", "shows consequences", "ties up loose ends"],
            "Resolution": ["concludes the journey", "reflects on growth", "sets future paths"]
        }
        chapter_event = random.choice(intensity_events.get(self.conflict_intensity, ["a critical moment"]))
        arc_context = random.choice(arc_events.get(arc_stage, ["advances the story"]))
        
        plot_point = ""
        if self.key_plot_points and random.random() < 0.2:
            plot_point = f"This chapter ties to {random.choice(self.key_plot_points).lower()}. "
        
        rel_desc = ""
        if len(characters_involved) >= 2 and characters_involved[1].name in characters_involved[0].relationships:
            rel_desc = f"Their {characters_involved[0].relationships[characters_involved[1].name].lower()} relationship shaped the encounter. "
        
        dev_event = f"{character_names[0]} {random.choice(['grew more determined', 'faced doubts', 'found new resolve', 'changed perspective'])} due to {chapter_event}."
        characters_involved[0].add_development(chapter_num, dev_event)
        
        chapter_content = f"""
## Chapter {chapter_num} ({arc_stage})

In {self.setting}, {character_names[0]} faced {chapter_event}, which {arc_context}. Driven by {characters_involved[0].motivations.lower()}, they navigated {self.genre.lower()} challenges. {character_names[1]}'s {characters_involved[1].personality.lower()} nature influenced the outcome. {rel_desc}{plot_point}

The {self.tone.lower()} atmosphere highlighted {', '.join(self.themes).lower()}. {character_names[0]}'s {characters_involved[0].physical_traits.lower()} played a role as they {random.choice(['confronted', 'evaded', 'collaborated with'])} {character_names[1]}.

This {self.conflict_intensity} moment advanced the {self.plot.split('.')[1].strip().lower()}, spanning ~{pages_per_chapter} pages of {self.genre.lower()} tension and character growth.
"""
        return chapter_content

    def generate_book(self):
        if not self.plot or not self.characters or not self.genre:
            return "Error: Please add characters, set book details, and generate a plot first."
        
        pages_per_chapter = self.page_count // self.chapter_count
        narrative_arc = ["Introduction", "Rising Action", "Climax", "Falling Action", "Resolution"]
        arc_length = self.chapter_count // len(narrative_arc)
        
        book_content = f"""
# {self.title}

*Genre*: {self.genre}  
*Setting*: {self.setting}  
*Tone*: {self.tone}  
*Themes*: {', '.join(self.themes)}  
*Conflict Intensity*: {self.conflict_intensity}  
*Page Count*: {self.page_count}  
*Chapter Count*: {self.chapter_count}  
*Key Plot Points*: {', '.join(self.key_plot_points) if self.key_plot_points else 'None'}  
*Created*: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Character Summaries
{''.join([c.get_summary() for c in self.characters])}

## Plot Summary
{self.plot}

## Chapters
"""
        for i in range(1, self.chapter_count + 1):
            arc_index = min((i - 1) // arc_length, len(narrative_arc) - 1)
            arc_stage = narrative_arc[arc_index]
            book_content += self.generate_chapter(i, pages_per_chapter, arc_stage)
        
        filename = f"output/{self.title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        try:
            os.makedirs("output", exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(book_content)
            export_message = f"\nBook saved as {filename}"
        except Exception as e:
            export_message = f"\nError saving book to file: {e}"
        
        return book_content + export_message

def main():
    print("Starting Book Generator...")
    check_environment()
    generator = BookGenerator()
    
    print("\nWelcome to the Book Generator!")
    print("Instructions:")
    print("- Add characters (minimum 2 required) with relationships.")
    print("- Set book details (genre, setting, tone, themes, page count, chapter count, conflict intensity, title, key plot points).")
    print("- Generate the plot based on characters and settings.")
    print("- Preview book structure (optional).")
    print("- Generate the full book (no modifications after generation, saved as Markdown).")
    print("- Type 'exit' to quit.")
    
    while True:
        print("\nOptions: add_character, set_details, generate_plot, preview_structure, generate_book, exit")
        choice = input("What would you like to do? ").lower().strip()
        
        if choice == "exit":
            print("Exiting Book Generator.")
            break
        
        elif choice == "add_character":
            print("\nEnter character details (leave non-required fields blank if desired):")
            try:
                name = input("Name: ").strip()
                age = input("Age: ").strip() or "0"
                gender = input("Gender: ").strip() or "Not specified"
                occupation = input("Occupation: ").strip() or "Not specified"
                personality = input("Personality: ").strip() or "Not specified"
                backstory = input("Backstory: ").strip() or "Not specified"
                physical_traits = input("Physical Traits: ").strip() or "Not specified"
                motivations = input("Motivations: ").strip() or "Not specified"
                print("Enter relationships (e.g., 'John: Friend, Jane: Enemy') or leave blank:")
                rel_input = input("Relationships: ").strip()
                relationships = {}
                if rel_input:
                    for rel in rel_input.split(","):
                        try:
                            char, rel_type = [x.strip() for x in rel.split(":")]
                            relationships[char] = rel_type
                        except ValueError:
                            raise ValueError("Invalid relationship format. Use 'Name: Type'.")
                summary = generator.add_character(name, age, gender, occupation, personality, backstory, physical_traits, motivations, relationships)
                print("\nCharacter Summary:")
                print(summary)
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error: Invalid input. {e}")
        
        elif choice == "set_details":
            print("\nEnter book details (all fields except plot points are required):")
            try:
                genre = input("Genre (e.g., Fantasy, Sci-Fi, Mystery, Romance, Thriller): ").strip()
                setting = input("Setting (e.g., Medieval Kingdom, Futuristic City): ").strip()
                tone = input("Tone (e.g., Dark, Hopeful, Suspenseful): ").strip()
                themes = input("Themes (comma-separated, e.g., Love, Betrayal, Redemption): ").strip()
                themes = themes.split(",") if themes else []
                page_count = input("Page Count (100-400): ").strip() or "100"
                chapter_count = input("Chapter Count (10-100): ").strip() or "10"
                conflict_intensity = input("Conflict Intensity (low, medium, high): ").strip() or "medium"
                title = input("Book Title: ").strip()
                print("Enter key plot points (comma-separated, e.g., 'Discover ancient relic, Final battle') or leave blank:")
                plot_points_input = input("Key Plot Points: ").strip()
                key_plot_points = [p.strip() for p in plot_points_input.split(",") if p.strip()] if plot_points_input else []
                result = generator.set_book_details(genre, setting, tone, themes, page_count, chapter_count, conflict_intensity, title, key_plot_points)
                print("\n" + result)
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error: Invalid input. {e}")
        
        elif choice == "generate_plot":
            plot = generator.generate_plot()
            print("\nGenerated Plot:")
            print(plot)
        
        elif choice == "preview_structure":
            preview = generator.preview_book_structure()
            print("\nBook Structure Preview:")
            print(preview)
        
        elif choice == "generate_book":
            book = generator.generate_book()
            print("\nGenerated Book:")
            print(book)
            print("\nBook generation complete. No further modifications allowed.")
            break
        
        else:
            print("Invalid option. Please choose: add_character, set_details, generate_plot, preview_structure, generate_book, exit")

if __name__ == "__main__":
    main()