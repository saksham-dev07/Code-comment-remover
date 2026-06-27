import re
import io
import tokenize
import ast

def remove_python_comments(source: str, remove_line: bool = True, preserve_docstrings: bool = False) -> str:
    docstring_nodes = []
    if not preserve_docstrings:
        try:
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
                    if (node.body and isinstance(node.body[0], ast.Expr)
                       and isinstance(node.body[0].value, ast.Constant)
                       and isinstance(node.body[0].value.value, str)):
                        doc_node = node.body[0].value
                        docstring_nodes.append(doc_node)
        except SyntaxError:
            pass
            
    try:
        tokens = list(tokenize.tokenize(io.BytesIO(source.encode('utf-8')).readline))
    except tokenize.TokenError:
        return source
        
    lines = source.splitlines(True)
    def get_offset(row, col):
        if row - 1 < len(lines):
            return sum(len(l) for l in lines[:row-1]) + col
        return len(source)
        
    remove_intervals = []
    
    for tok in tokens:
        if tok.type == tokenize.COMMENT and remove_line:
            start_off = get_offset(*tok.start)
            end_off = get_offset(*tok.end)
            remove_intervals.append((start_off, end_off))
            
    for doc in docstring_nodes:
        if hasattr(doc, 'lineno') and hasattr(doc, 'end_lineno'):
            for tok in tokens:
                if tok.type == tokenize.STRING and tok.start[0] == doc.lineno:
                    start_off = get_offset(*tok.start)
                    end_off = get_offset(*tok.end)
                    remove_intervals.append((start_off, end_off))
                    break
                    
    remove_intervals.sort()
    
    if not remove_intervals:
        return source
        
    out = []
    last_idx = 0
    for start, end in remove_intervals:
        if start >= last_idx:
            out.append(source[last_idx:start])
            last_idx = end
    out.append(source[last_idx:])
    
    cleaned_source = "".join(out)
    
    # Remove any empty lines created by removals, but preserve others
    # Wait, simple way is to just let them be, or use a basic trailing whitespace cleanup
    cleaned_source = re.sub(r'[ \t]+$', '', cleaned_source, flags=re.MULTILINE)
    
    return cleaned_source


def remove_css_js_comments(source: str, remove_block: bool = True, remove_line: bool = True) -> str:
    pattern = r"""
        (?P<string>
            "(?:\\.|[^"\\])*" |
            '(?:\\.|[^'\\])*' |
            `(?:\\.|[^`\\])*`
        ) |
        (?P<block>/\*.*?\*/) |
        (?P<line>//[^\r\n]*)
    """
    regex = re.compile(pattern, re.VERBOSE | re.DOTALL)
    
    def replacer(match):
        if match.group('string') is not None:
            return match.group('string')
        elif match.group('block') is not None:
            return '' if remove_block else match.group('block')
        elif match.group('line') is not None:
            return '' if remove_line else match.group('line')
        return match.group(0)
        
    return regex.sub(replacer, source)


def remove_html_comments(source: str) -> str:
    return re.sub(r'<!--[\s\S]*?-->', '', source)


def detect_language(source: str, filename: str) -> str:
    ext = filename.lower().rsplit('.', 1)[-1]
    if ext == 'py' or (source.startswith('#!') and 'python' in source):
        return 'py'
    if ext == 'js':
        return 'js'
    if ext == 'css':
        return 'css'
    if ext in ['html', 'htm'] or '<html' in source.lower():
        return 'html'
    return 'js'
