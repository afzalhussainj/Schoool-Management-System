from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates/'))
template = env.get_template('pswd_reset_email.html')

def pswdResetEmailTemplate():
    content = template.render(
        
    )