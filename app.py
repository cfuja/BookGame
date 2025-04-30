import random
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file
from io import BytesIO

app = Flask(__name__)

class Character:
    def __init__(self, name, age, gender, occupation, personality, backstory, physical_traits, motivations, relationships):
        self.name = name
        self.age = age
        self.gender = gender
        self.occupation = occupation
        self.personality = personality
        self.backstory = backstory
        self.physical_traits = physical_traits
        self.motivations = motivations
        self.relationships = relationships
        self.development = []

    def get_summary(self):
        rel_str = "<br>".join([f"&nbsp;&nbsp;- {char}: {rel}" for char, rel in self.relationships.items()]) if self.relationships else "None"
        dev_str = "<br>".join(self.development) if self.development else "No development yet."
        return f"""
Name: {self.name}<br>
Age: {self.age}<br>
Gender: {self.gender}<br>
Occupation: {self.occupation}<br>
Personality: {self.personality}<br>
Backstory: {self.backstory}<br>
Physical Traits: {self.physical_traits}<br>
Motivations: {self.motivations}<br>
Relationships:<br>{rel_str}<br>
Development:<br>{dev_str}
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
        age = self.validate_integer(age, "Age", min_val=0)
        name = self.validate_non_empty_string(name, "Name")
        character = Character(name, age, gender, occupation, personality, backstory, physical_traits, motivations, relationships)
        self.characters.append(character)
        return character.get_summary()

    def set_book_details(self, genre, setting, tone, themes, page_count, chapter_count, conflict_intensity, title, key_plot_points):
        self.genre = self.validate_non_empty_string(genre, "Genre")
        self.setting = self.validate_non_empty_string(setting, "Setting")
        self.tone = self.validate_non_empty_string(tone, "Tone")
        self.themes = [t.strip() for t in themes.split(",") if t.strip()]
        if not self.themes:
            raise ValueError("At least one theme is required.")
        self.page_count = self.validate_integer(page_count, "Page Count", min_val=100, max_val=400)
        self.chapter_count = self.validate_integer(chapter_count, "Chapter Count", min_val=10, max_val=100)
        self.conflict_intensity = conflict_intensity.lower()
        if self.conflict_intensity not in ["low", "medium", "high"]:
            raise ValueError("Conflict intensity must be low, medium, or high.")
        self.title = self.validate_non_empty_string(title, "Title")
        self.key_plot_points = [p.strip() for p in key_plot_points.split(",") if p.strip()]
        return "Book details set successfully!"

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
In {self.setting}, {protagonist.name}, a {protagonist.occupation}, embarks on a {self.tone} journey driven by {protagonist.motivations.lower()}.<br>
The story revolves around {intensity_desc} {conflict}. {antagonist.name if antagonist else 'An opposing force'}, motivated by {antagonist.motivations.lower() if antagonist else 'conflicting goals'}, creates obstacles.<br>
{rel_desc}{plot_points_desc}Key themes include {', '.join(self.themes)}.<br>
The narrative unfolds through {protagonist.name}'s perspective, with {self.conflict_intensity} stakes shaped by {self.genre.lower()} elements.
"""
        return self.plot

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
## Chapter {chapter_num} ({arc_stage})<br><br>
In {self.setting}, {character_names[0]} faced {chapter_event}, which {arc_context}. Driven by {characters_involved[0].motivations.lower()}, they navigated {self.genre.lower()} challenges. {character_names[1]}'s {characters_involved[1].personality.lower()} nature influenced the outcome. {rel_desc}{plot_point}<br><br>
The {self.tone.lower()} atmosphere highlighted {', '.join(self.themes).lower()}. {character_names[0]}'s {characters_involved[0].physical_traits.lower()} played a role as they {random.choice(['confronted', 'evaded', 'collaborated with'])} {character_names[1]}.<br><br>
This {self.conflict_intensity} moment advanced the {self.plot.split('.')[1].strip().lower()}, spanning ~{pages_per_chapter} pages of {self.genre.lower()} tension and character growth.<br>
"""
        return chapter_content

    def generate_book(self):
        if not self.plot or not self.characters or not self.genre:
            return "Error: Please add characters, set book details, and generate a plot first."
        
        pages_per_chapter = self.page_count // self.chapter_count
        narrative_arc = ["Introduction", "Rising Action", "Climax", "Falling Action", "Resolution"]
        arc_length = self.chapter_count // len(narrative_arc)
        
        book_content = f"""
# {self.title}<br><br>
*Genre*: {self.genre}<br>
*Setting*: {self.setting}<br>
*Tone*: {self.tone}<br>
*Themes*: {', '.join(self.themes)}<br>
*Conflict Intensity*: {self.conflict_intensity}<br>
*Page Count*: {self.page_count}<br>
*Chapter Count*: {self.chapter_count}<br>
*Key Plot Points*: {', '.join(self.key_plot_points) if self.key_plot_points else 'None'}<br>
*Created*: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br><br>
## Character Summaries<br>
{''.join([c.get_summary() for c in self.characters])}<br>
## Plot Summary<br>
{self.plot}<br>
## Chapters<br>
"""
        for i in range(1, self.chapter_count + 1):
            arc_index = min((i - 1) // arc_length, len(narrative_arc) - 1)
            arc_stage = narrative_arc[arc_index]
            book_content += self.generate_chapter(i, pages_per_chapter, arc_stage)
        
        return book_content

generator = BookGenerator()
output = ""
book_content = ""

@app.route("/", methods=["GET", "POST"])
def index():
    global output, book_content
    if request.method == "POST":
        action = request.form.get("action")
        try:
            if action == "add_character":
                name = request.form.get("name", "")
                age = request.form.get("age", "0")
                gender = request.form.get("gender", "Not specified")
                occupation = request.form.get("occupation", "Not specified")
                personality = request.form.get("personality", "Not specified")
                backstory = request.form.get("backstory", "Not specified")
                physical_traits = request.form.get("physical_traits", "Not specified")
                motivations = request.form.get("motivations", "Not specified")
                relationships = {}
                rel_input = request.form.get("relationships", "")
                if rel_input:
                    for rel in rel_input.split(","):
                        if ":" in rel:
                            char, rel_type = [x.strip() for x in rel.split(":")]
                            relationships[char] = rel_type
                output = generator.add_character(name, age, gender, occupation, personality, backstory, physical_traits, motivations, relationships)
            
            elif action == "set_details":
                genre = request.form.get("genre", "")
                setting = request.form.get("setting", "")
                tone = request.form.get("tone", "")
                themes = request.form.get("themes", "")
                page_count = request.form.get("page_count", "100")
                chapter_count = request.form.get("chapter_count", "10")
                conflict_intensity = request.form.get("conflict_intensity", "medium")
                title = request.form.get("title", "")
                key_plot_points = request.form.get("key_plot_points", "")
                output = generator.set_book_details(genre, setting, tone, themes, page_count, chapter_count, conflict_intensity, title, key_plot_points)
            
            elif action == "generate_plot":
                output = generator.generate_plot()
            
            elif action == "preview_structure":
                output = generator.preview_book_structure().replace("\n", "<br>")
            
            elif action == "generate_book":
                book_content = generator.generate_book()
                output = "Book generated! Download below."
            
            elif action == "download_book" and book_content:
                buffer = BytesIO(book_content.encode('utf-8'))
                filename = f"{generator.title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                return send_file(buffer, as_attachment=True, download_name=filename, mimetype="text/markdown")
        
        except ValueError as e:
            output = f"Error: {e}"
        except Exception as e:
            output = f"Error: Invalid input. {e}"
        
        return render_template("index.html", output=output, book_generated=bool(book_content))
    
    return render_template("index.html", output=output, book_generated=bool(book_content))

if __name__ == "__main__":
    app.run(debug=True)