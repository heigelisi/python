# mistune   --Markdown 解析成html
#pygments  --Markdown 高亮显示code
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)

renderer = HighlightRenderer()
markdown = mistune.Markdown(renderer=renderer)
with open("体态检测文档.md","r",encoding="utf-8") as f:
    code = f.read()

with open("体态检测文档.html","w",encoding="utf-8") as f:
    f.write(markdown(code))



# print(markdown('```python\nassert 1 == 1\n```'))