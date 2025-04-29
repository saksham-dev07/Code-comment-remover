import re
import io
import tokenize
import ast

def remove_python_comments(
    source: str,
    remove_line: bool = True,
    preserve_docstrings: bool = False
) -> str:
    """
    - remove_line: whether to strip `# ...` comments
    - preserve_docstrings: if False, also strip docstrings via AST
    """
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    filtered = []
    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            if remove_line:
                continue
            else:
                filtered.append((tok.type, tok.string))
        else:
            filtered.append((tok.type, tok.string))

    code = tokenize.untokenize(filtered)
    if preserve_docstrings:
        return code

    # strip docstrings
    class DocRemover(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            self.generic_visit(node)
            if (node.body and isinstance(node.body[0], ast.Expr)
               and isinstance(node.body[0].value, ast.Constant)
               and isinstance(node.body[0].value.value, str)):
                node.body.pop(0)
            return node

        def visit_ClassDef(self, node):
            self.generic_visit(node)
            if (node.body and isinstance(node.body[0], ast.Expr)
               and isinstance(node.body[0].value, ast.Constant)
               and isinstance(node.body[0].value.value, str)):
                node.body.pop(0)
            return node

        def visit_Module(self, node):
            self.generic_visit(node)
            if (node.body and isinstance(node.body[0], ast.Expr)
               and isinstance(node.body[0].value, ast.Constant)
               and isinstance(node.body[0].value.value, str)):
                node.body.pop(0)
            return node

    tree = ast.parse(code)
    cleaned_tree = DocRemover().visit(tree)
    return ast.unparse(cleaned_tree)


def remove_css_js_comments(
    source: str,
    remove_block: bool = True,
    remove_line: bool = True
) -> str:
    if remove_block:
        source = re.sub(r'/\*[\s\S]*?\*/', '', source)
    if remove_line:
        source = re.sub(r'//.*', '', source)
    return source


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
