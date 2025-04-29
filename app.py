import os
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
from comment_utils import (
    remove_python_comments,
    remove_css_js_comments,
    remove_html_comments,
    detect_language
)

app = Flask(__name__)
CORS(app)

SETTINGS_PATH = os.path.join(app.root_path, 'settings.json')
DEFAULT_SETTINGS = {
    'py_line': True,
    'py_doc': False,
    'js_block': True,
    'js_line': True,
    'html_comment': True
}

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, 'r') as f:
            return {**DEFAULT_SETTINGS, **json.load(f)}
    return DEFAULT_SETTINGS.copy()

def save_settings(settings_dict):
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings_dict, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html', current_year=datetime.now().year)

@app.route('/settings', methods=['GET','POST'])
def settings():
    if request.method == 'POST':
        user_settings = request.get_json(force=True)
        save_settings(user_settings)
        return jsonify(success=True)
    else:
        current = load_settings()
        return render_template(
            'settings.html',
            current_year=datetime.now().year,
            settings=current
        )

@app.route('/api/remove', methods=['POST'])
def api_remove():
    data = request.get_json(force=True)
    files = data.get('files', [])
    client_rules = data.get('rules', {})
    server_rules = load_settings()
    # client overrides server defaults:
    rules = { **server_rules, **client_rules }

    output = {}
    stats = []
    for f in files:
        name, content = f['name'], f['content']
        lang = detect_language(content, name)

        if lang == 'py':
            cleaned = remove_python_comments(
                content,
                remove_line=rules['py_line'],
                preserve_docstrings=rules['py_doc']
            )
        elif lang in ['js', 'css']:
            cleaned = remove_css_js_comments(
                content,
                remove_block=rules['js_block'],
                remove_line=rules['js_line']
            )
        elif lang == 'html':
            if rules['html_comment']:
                cleaned = remove_html_comments(content)
            else:
                cleaned = content
        else:
            cleaned = content

        output[name] = cleaned
        orig_lines = content.count("\n") + 1
        clean_lines = cleaned.count("\n") + 1
        stats.append({
            'name': name,
            'original_lines': orig_lines,
            'cleaned_lines': clean_lines,
            'removed': orig_lines - clean_lines
        })

    return jsonify({'files': output, 'stats': stats})

if __name__ == '__main__':
    app.run(debug=True)
