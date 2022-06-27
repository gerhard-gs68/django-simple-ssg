from os import PathLike
import re
from pathlib import Path

class BraTmpl():
    """Compile an text into a template function"""

    def __init__(self, text):
        self.delimiter = re.compile(r'<\|(.*?)\|>', re.DOTALL)
        self.set_text(text)
        self.global_context = dict()


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


    def render(self, context = None, mode = 'django', **kw):
        """Render the template according to the given global_context"""
        if context:
            self.global_context.update(context)
        if kw:
            self.global_context.update(kw)

        result = []
        for is_code, token in self.tokens:
            if is_code:
                token = token.strip()

                mini_token_list = token.split('|')
                
                command = mini_token_list[0].strip()
            
                # replace snippets 
                if command == 'snippet':
                    result.append(self.global_context[mini_token_list[1]])
                # content inside command django is only included if mode is django
                elif command == 'django' and mode=='django':
                    result.append(mini_token_list[1])
                else:
                    result.append('<!!!Something wrong with BraTmpl!!!>')
            else:
                result.append(token)
        return ''.join(result)

    #def

    # make instance callable
    __call__ = render

if __name__ == '__main__':
    t = BraTmpl("Das ist <?! snippet intro_carousel.html !?> vom ")
    t.read_snippets('./CONTENT/snippets')
    #print(t.global_context)
    print(t.render())
