from os import PathLike
import re
from pathlib import Path

class SmplTmplt():
    """Compile an text into a template function"""

    def __init__(self, text):
        self.delimiter = re.compile(r'\{\?!(.*?)!\?\}', re.DOTALL)
        self.tokens = self.compile(text)
        self. global_context = dict()


    def set_text(self, text):
        self.tokens = self.compile(text)


    def read_snippets(self, snippets_dir):
        if type(snippets_dir) is not Path:
            snippets_dir = Path(snippets_dir)

        for child in snippets_dir.iterdir():
            file_name = child.name

            with open(child) as f:
                snippet = f.read()
                self.global_context[file_name] = snippet


    def compile(self, text):
        tokens = []
        for index, token in enumerate(self.delimiter.split(text)):
            if index % 2 == 0:  
                if token:
                    tokens.append((False, token.replace('%\}', '%}').replace('{\%', '{%')))
            else:
                tokens.append((True, token))

        return tokens


    def render(self, context = None, **kw):
        """Render the template according to the given global_context"""
        if context:
            self.global_context.update(context)
        if kw:
            self.global_context.update(kw)

        result = []
        for is_code, token in self.tokens:
            if is_code:
                token = token.strip()

                mini_token_list = token.split()
                
                command = mini_token_list[0]
                
                if command == 'snippet':
                    result.append(self.global_context[mini_token_list[1]])
                else:
                    result.append('Missing ')
            else:
                result.append(token)
        return ''.join(result)

    #def

    # make instance callable
    __call__ = render

if __name__ == '__main__':
    t = SmplTmplt("Das ist <?! snippet intro_carousel.html !?> vom ")
    t.read_snippets('./CONTENT/snippets')
    #print(t.global_context)
    print(t.render())
