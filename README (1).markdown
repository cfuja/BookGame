# Book Generator Web

A web-based application built with Flask to generate customizable books. Users can add characters, set book details, generate a plot, preview the structure, and produce a full book (100–400 pages, 10–100 chapters) displayed on-screen and downloadable as Markdown.

## Features
- Add characters with detailed attributes and relationships.
- Customize book details (genre, setting, tone, themes, page count, chapter count, conflict intensity, title, key plot points).
- Generate a plot based on characters and settings.
- Preview the book structure with chapter outlines.
- Generate a complete book with a narrative arc, viewable in the browser and downloadable.
- Responsive, user-friendly interface with error handling.

## Prerequisites
- Python 3.8+
- Git
- Heroku CLI (for deployment)

## Setup (Local)
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/book-generator-web.git
   cd book-generator-web
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in a browser.

## Deployment (Heroku)
1. Ensure the repository is set up as above.
2. Login to Heroku:
   ```bash
   heroku login
   heroku create book-generator-web
   ```
3. Deploy:
   ```bash
   git push heroku main
   ```
4. Open the app:
   ```bash
   heroku open
   ```

## Project Structure
```
book-generator-web/
├── app.py
├── templates/
│   ├── index.html
│   ├── add_character.html
│   ├── set_details.html
│   └── book_display.html
├── static/
│   └── style.css
├── output/
├── requirements.txt
├── Procfile
└── README.md
```

## Usage
1. Navigate to the home page (`/`).
2. Use the navigation to:
   - **Add Character**: Enter character details (Name and Age required).
   - **Set Book Details**: Specify book attributes (most fields required).
   - **Generate Plot**: Create a plot summary.
   - **Preview Structure**: View the book outline.
   - **Generate Book**: Produce the full book, displayed on a dedicated page.
3. On the book display page, view the book and download it as a Markdown file.
4. Errors and success messages appear on the home page.

## Troubleshooting
- **Blank page or no interface**: Ensure Flask is installed and the server is running (`python app.py`).
- **404 errors**: Verify all files are in the correct directories (`templates/`, `static/`).
- **Book not generating**: Add at least 2 characters and set book details first.
- **Deployment issues**: Check Heroku logs (`heroku logs --tail`) and ensure `Procfile` and `requirements.txt` are correct.

## License
MIT License. See `LICENSE` file (not included in this template).

## Contributing
Fork the repository, make changes, and submit a pull request.