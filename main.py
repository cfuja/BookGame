from book_generator import BookGenerator

def main():
    generator = BookGenerator()
    
    print("Welcome to the Book Generator!")
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
            print("\nEnter character details:")
            try:
                name = input("Name: ").strip()
                if not name:
                    raise ValueError("Name cannot be empty.")
                age = input("Age: ")
                gender = input("Gender: ")
                occupation = input("Occupation: ")
                personality = input("Personality: ")
                backstory = input("Backstory: ")
                physical_traits = input("Physical Traits: ")
                motivations = input("Motivations: ")
                print("Enter relationships (e.g., 'John: Friend, Jane: Enemy') or leave blank:")
                rel_input = input("Relationships: ").strip()
                relationships = {}
                if rel_input:
                    for rel in rel_input.split(","):
                        char, rel_type = [x.strip() for x in rel.split(":")]
                        relationships[char] = rel_type
                summary = generator.add_character(name, age, gender, occupation, personality, backstory, physical_traits, motivations, relationships)
                print("\nCharacter Summary:")
                print(summary)
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error: Invalid input. {e}")
        
        elif choice == "set_details":
            print("\nEnter book details:")
            try:
                genre = input("Genre (e.g., Fantasy, Sci-Fi, Mystery, Romance, Thriller): ")
                setting = input("Setting (e.g., Medieval Kingdom, Futuristic City): ")
                tone = input("Tone (e.g., Dark, Hopeful, Suspenseful): ")
                themes = input("Themes (comma-separated, e.g., Love, Betrayal, Redemption): ").split(",")
                themes = [t.strip() for t in themes if t.strip()]
                page_count = input("Page Count (100-400): ")
                chapter_count = input("Chapter Count (10-100): ")
                conflict_intensity = input("Conflict Intensity (low, medium, high): ")
                title = input("Book Title: ").strip()
                if not title:
                    raise ValueError("Title cannot be empty.")
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