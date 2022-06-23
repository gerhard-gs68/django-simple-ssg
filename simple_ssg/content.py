from django.conf import settings

from datetime import datetime
import subprocess
import shutil

from simple_ssg.smpl_tmplt_lng import SmplTmplt


class Content:
    """ Handles all kramdowncontent
    """
    def __init__(self):
        self.content_path = settings.BASE_DIR / 'CONTENT'
        self.assets_path = self.content_path / 'assets'
        self.kd_docs_path = self.content_path / 'kd_docs' 
        self.snippets_path = self.content_path / 'snippets'
        self.tmp_path = self.content_path / 'tmp'
        self.static_path = settings.BASE_DIR / settings.STATIC_URL.strip('/') # / around static url is confusing PATH
        print(settings.BASE_DIR , settings.STATIC_URL.strip('/'), settings.BASE_DIR / settings.STATIC_URL.strip('/'))
    
    def get_content_path(self):
        return self.content_path


    def handle_assets(self):
        print(f"{datetime.now()} -- ", "Handling assets folder.")

        # handle static folder
        print(self.static_path / 'assets')
        shutil.rmtree(self.static_path / 'assets')
        shutil.copytree(self.assets_path, self.static_path / 'assets', dirs_exist_ok=True)

        # handle out folder
        shutil.rmtree(self.content_path / 'out')
        shutil.copytree(self.assets_path, self.content_path / 'out' / 'assets', dirs_exist_ok=True)

    
    def handle_snippets(self, tmp, template):
        print(f"{datetime.now()} -- Handling snippets for {tmp}.")

        out = self.content_path / "out" / tmp.name

        with open(tmp) as tf, open(out, 'w') as wf:
            text = tf.read()
            template.set_text(text)
            rendered_text = template.render() 
            wf.write(rendered_text)   


    def handle_kddocs(self):
        print(f"{datetime.now()} -- ",   "Handling kramdown documents folder.") 

        t = SmplTmplt('')
        t.read_snippets(self.snippets_path)

        for child in self.kd_docs_path.iterdir():
            file_name = child.name.strip(".kd")
            tmplte = self.content_path / "templates/bs5-tmpl.html"
            tmp = self.content_path / "tmp" / (file_name + ".html")
            
            cmd=f"kramdown --template={tmplte} {child} > {tmp}"                                                                  
            p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)                               
            output, errors = p.communicate()         
            print(output, errors )               
             
            self.handle_snippets(tmp, t)


    def handle_content(self) :
        """ Takes the source files processes them through kramdown and
            put the processed files into the templates (kd files) or 
            static directory (all the rest).
        """
        print(f"Processing content folder {self.get_content_path()}") 
        self.handle_assets()

        # snippets are handled inside 
        self.handle_kddocs()

    