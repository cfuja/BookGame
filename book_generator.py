import random
from datetime import datetime
import os
from character import Character

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

    def add_character(self, name, age, gender, occupation, personality, backstory, physical_traits, motivations, relationships):
        try:
            age = int(age)
            if age < 0:
                raise ValueError("Age cannot be negative.")
            character = Character(name, age, gender, occupation, personality, backstory, physical_traits, motivations, relationships)
            self.characters.append(character)
            return character.get_summary()
        except ValueError as e:
            return f"Error: {e}"

    def set_book_details(self, genre, setting, tone, themes, page_count, chapter_count, conflict_intensity, title, key_plot_points):
        try:
            self.genre = genre
            self.setting = setting
            self.tone = tone
            self.themes = themes
            self.page_count = max(100, min(400, int(page_count)))
            self.chapter_count = max(10, min(100, int(chapter_count)))
            self.conflict_intensity = conflict_intensity.lower()
            if self.conflict_intensity not in ["low", "medium", "high"]:
                raise ValueError("Conflict intensity must be low, medium, or high.")
            self.title = title
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