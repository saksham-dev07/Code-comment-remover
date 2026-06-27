
# Code Comment Remover

A sleek, professional, and blazingly fast web application that strips comments and docstrings from your source code. Built with Python, Flask, and a high-contrast modern SaaS frontend.

## Features

- **Multi-Language Support**: Precisely removes comments from Python, JavaScript, CSS, and HTML.
- **AST Parsing (Python)**: Uses Python's built-in `ast` and `tokenize` modules to intelligently strip comments while avoiding accidental removals inside strings or valid code logic.
- **Regex Parsing (JS/CSS/HTML)**: Highly tuned regular expressions designed to safely strip block and inline comments from web assets.
- **Customizable Rules**: Fine-tune your cleaning process via the interactive Settings UI:
  - Toggle preservation of Python docstrings.
  - Choose between removing block comments, inline comments, or both.
  - Export and import your custom configurations.
- **Batch Processing**: Drag and drop multiple files at once.
- **Dark Mode Native UI**: A premium frontend with automatic Dark/Light mode support.

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/code-comment-remover.git
   cd code-comment-remover
   ```

2. **Set up a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

Start the Flask server by running the included batch script (Windows) or executing Python directly:

```bash
python app.py
```

The application will be available at `http://localhost:5000`.

## Tech Stack

- **Backend**: Python 3, Flask, Werkzeug
- **Frontend**: Vanilla HTML/JS, Modern CSS (CSS Variables, Flexbox/Grid), Bootstrap 5 (for utility classes), Prism.js (Syntax highlighting).
- **Icons**: Bootstrap Icons
- **Fonts**: Inter

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
=======
