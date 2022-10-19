from django.conf import settings

from bs4 import BeautifulSoup
from datetime import datetime
import frontmatter
import subprocess
import shutil
import sys


from simple_ssg.bratmpl.bratmpl import BraTmpl


class Content:
    """ Handles all kramdowncontent
    """
    def __init__(self):
        self.main_app_path = settings.MAIN_APP_DIR
        self.dj_tmplt_path = self.main_app_path / 'templates'

        self.content_path = settings.BASE_DIR / 'CONTENT'
        self.assets_path = self.content_path / 'assets'
        self.kd_templates_path = self.content_path / 'templates'
        self.kd_docs_path = self.content_path / 'kd_docs' 
        self.snippets_path = self.content_path / 'snippets'
        self.variables_file = self.content_path / 'variables.yaml'
        self.tmp_path = self.content_path / 'tmp'
        self.static_path = settings.BASE_DIR / settings.STATIC_URL.strip('/') 
        # / around static url is confusing PATH
        print(settings.BASE_DIR , settings.STATIC_URL.strip('/'), settings.BASE_DIR / settings.STATIC_URL.strip('/'))
        self.mode = 'django'

    def get_content_path(self):
        return self.content_path


    def handle_assets(self):
        print(f"{datetime.now()} -- ", "Handling assets folder.")

        # handle static folder
        shutil.rmtree(self.static_path / 'assets')
        shutil.copytree(self.assets_path, self.static_path / 'assets', dirs_exist_ok=True)

        # handle out folder
        shutil.rmtree(self.content_path / 'out')
        shutil.copytree(self.assets_path, self.content_path / 'out' / 'assets', dirs_exist_ok=True)

    
    def handle_static_links(self, text):
        print(f"{datetime.now()} -- Handling static links for {text[0:100]} for django or others.")


        def has_href_src_etc(tag):
            return tag.has_attr('href')  or tag.has_attr('src')


        #print("+++++++++++++++++++++++++++++++++++++++++++++") 
       
        soup = BeautifulSoup(text, 'html.parser')

        relevant_tags = soup.find_all(has_href_src_etc)

        for attrib in ['href', 'src']:
            for tag in relevant_tags:
                if tag.has_attr(attrib) and tag[attrib].startswith('static/') :
                    #print(tag[attrib])
                    t = tag[attrib][len('static/'):]
                    if self.mode == 'django':
                        tag[attrib] = f"{{% static '{t}' %}}"
                        #print(tag[attrib])
                
        #print("+++++++++++++++++++++++++++++++++++++++++++++") 
        return str(soup)

    
    def handle_braket(self, kd_file, template):
        print(f"{datetime.now()} -- Handling snippets for {kd_file}.")
        
        rel_path_to_kddocs = kd_file.relative_to(self.kd_docs_path)
  
        file_out = self.content_path / "tmp" / str(rel_path_to_kddocs)
        fileout_path = file_out.parent

        fileout_path.mkdir(parents=True, exist_ok=True)
        with open(kd_file) as tf, open(file_out, 'w') as wf:
            text = tf.read()

            post_yaml = frontmatter.loads(text)
            
            template.set_text(post_yaml.content)
            rendered_text = template.render() 
  
            wf.write(rendered_text)   

        return post_yaml, file_out


    def handle_dj_tmplts(self, name, completly_processed_kd_file, gen_view_code, gen_view=True):
        ""
        print(f"{datetime.now()} -- ",   "Handling kramdown documents to django.") 
        

        rel_path = completly_processed_kd_file.relative_to(self.content_path / "out")

        dest = self.dj_tmplt_path / str(rel_path)
        dest_path = dest.parent
        dest_path.mkdir(parents=True, exist_ok=True)
        shutil.copy2(completly_processed_kd_file, dest)

        if not gen_view:
            return gen_view_code

        gen_view_code += f"""
def {name}(request):
    return render(request, '{str(rel_path)}')  
        
view_objects['{name}'] = {name}


"""
     
        return gen_view_code
        


    def handle_kddocs(self):
        print(f"\n{datetime.now()} -- ",   "Handling kramdown documents folder.") 

        t = BraTmpl('')
        t.read_snippets(self.snippets_path)
        t.read_variables(self.variables_file)

        # prepare the kramdown templates 
        self.handle_kd_templates(t)

        # some initialization of the django templates and views
        gen_view_code = """
'''

THIS IS AN AUTOGENERATED FILE DO NOT EDIT

'''
from django.shortcuts import render

view_objects = dict()


"""

        for child in self.kd_docs_path.rglob("*.md"):
            file_name = child.stem
            print(f"\n{datetime.now()} -- Handling kramdown document {file_name}") 
            
            #print(child)
            rel_path = child.relative_to(self.kd_docs_path)
           
            post, processed_kd_file = self.handle_braket(child, t)

            tmplte = self.content_path / f"ptml/{post['md_template']}"
            out = self.content_path / "out" / str(rel_path.parent) /(file_name + ".html")
            out_path = out.parent

            out_path.mkdir(parents=True, exist_ok=True)
            cmd=f"kramdown --template={tmplte} {processed_kd_file} > {out}"    
            #cmd=f"kramdown  {processed_kd_file} > {out}"                                                                
            p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)      
            output, errors = p.communicate()         
            print(output, errors )               

            # process static links depening on targets
            with open(out) as tf:
                text = tf.read()
                proccessed_text = self.handle_static_links(text)

            with open(out, 'w') as wf:
                wf.write(proccessed_text)


            
            # now use the processed file to gen the template and the views
            gen_view_code = self.handle_dj_tmplts(file_name, completly_processed_kd_file=out, 
                                             gen_view_code=gen_view_code, 
                                             gen_view=post['gen_view'])

        with open(self.main_app_path / 'gen_views.py', 'w') as wf:
            wf.write(gen_view_code)   

       


    def handle_kd_templates(self, template):
        print(f"{datetime.now()} -- ",   "Preprocess kramdown templates folder.") 

        t = template
    
        for child in self.kd_templates_path.iterdir():
            
            file_name = child.name

            p_tmplte = self.content_path / "ptml"

            with open(child) as tf, open(p_tmplte / file_name, 'w') as wf:
                text = tf.read()
                
                t.set_text(text)
                rendered_text = t.render() 
                wf.write(rendered_text)   
    


    def handle_content(self) :
        """ Takes the source files processes them through kramdown and
            put the processed files into the templates (kd files) or 
            static directory (all the rest).
        """
        print(f"Processing content folder {self.get_content_path()}") 
        self.handle_assets()

        # snippets are handled inside 
        self.handle_kddocs()

    