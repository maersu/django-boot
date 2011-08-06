import os, sys, re, commands
from fabric.api import *
from fabric.contrib.console import *
from fabric.contrib.project import *
from fabric.contrib.files import contains, exists
import fileinput
from random import choice

env.this_file = os.path.join(os.path.dirname(os.path.abspath(__file__)))
env.template_folder = os.path.join(env.this_file, 'templates')

def _setlocal_env(projectpath):
    if not env.has_key('projectpath'):    
        env.projectpath = os.path.normpath(projectpath)
        split_path = os.path.split(env.projectpath)
        env.projectname = split_path[-1]
        env.projecthome_path = split_path[0]
        env.projectenvpath = env.projectpath + '-env'
        env.parentfolder = os.path.split(env.projecthome_path)[-1]

def _check_exists_skip(path):
    if os.path.exists(path):
        if prompt('Path %s already exists. Overwrite? ' % path, default='no') == 'yes':
            local("rm -rf '%s'" % path)
        else:
            warn('skip step')
            return True
    return False

def _create_from_template(root_path, templates):
    for template in templates:
        dirpath = os.path.join(root_path, template[0])
        if template[0]:
            local("mkdir -p %s" % dirpath)
        if len(template) > 1 and template[1]:
            template_path = os.path.join(env.template_folder,template[1])
            
            if os.path.exists(template_path):
                local("cp %s %s" % (template_path , dirpath))
            else:
                local("touch %s" % (os.path.join(dirpath,template[1])))
        
PROJECT_TEMPLATE = [
    ('compass/config', 'config.rb'),
    ('compass/config/sass', '.keep'),
    ('db', '.keep'),
    ('log', '.keep'),
    ('src',),
    ('log', '.keep'),
    ('', 'dep.pip'),
    ('', 'README.rst'),
    ('', '.gitignore')    
]

SRC_TEMPLATE = [
    ('media/css/', '.keep'),
    ('media/img/', '.keep'),
    ('media/js/', '.keep'),
    ('', 'settings_local.py'),
    ('', 'urls.py'),    
    ('', 'settings.py'),    
    ('', 'runserver.sh'),  
]

def bootstrap(projectpath):
    virtualenv(projectpath)
    
    if _check_exists_skip(projectpath) == False:
        _setlocal_env(projectpath)
        _create_from_template(projectpath, PROJECT_TEMPLATE)
        print local('/bin/bash -c " cd %(projectpath)s/src && source %(projectenvpath)s/bin/activate && django-admin.py startproject %(projectname)s"' % env)
        _create_from_template(os.path.join(projectpath,'src', env.projectname), SRC_TEMPLATE)
           
        replace_dict = {'projectpath': env.projectpath, 'projectname': env.projectname, 
                        'parentfolder': env.parentfolder, 'projectenvpath': env.projectenvpath,
                        'projectsecret': ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])}
        def _replace_in_files(arg, dirname, names):
            for name in names:
                filepath =  os.path.join(dirname, name)            
                if os.path.isfile(filepath):
                    for line in fileinput.input(filepath,inplace=1):
                        for key, value in replace_dict.items():
                            line = line.replace("{{%s}}" % key, value)
                        sys.stdout.write(line)      
        os.path.walk(env.projectpath, _replace_in_files, None)
        local("cp %(template_folder)s/dep.pip %(projectpath)s/" % env)
        
def virtualenv(projectpath):
    _setlocal_env(projectpath)
    if _check_exists_skip(env.projectenvpath) == False:
        print local("virtualenv --no-site-packages %(projectenvpath)s" % env)
        local("mkdir %(projectenvpath)s/lib/pkgconfig/" % env)
        local("ln -s %(projectenvpath)s/lib %(projectenvpath)s/lib64" % env)
        
    pip(projectpath)

def pip(projectpath):
    _setlocal_env(projectpath)
    if os.path.exists(env.projectpath):
        pip_path = env.projectpath
    else:
        pip_path = env.template_folder
        
    print local('/bin/bash -c "source %s/bin/activate && pip install pip pyinotify && pip install -r %s/dep.pip"' % (env.projectenvpath, pip_path))
        
     