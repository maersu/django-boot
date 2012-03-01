import os, sys, re, commands
from fabric.api import *
from fabric.contrib.console import *
from fabric.contrib.project import *
from fabric.contrib.files import exists
from fabric.utils import warn
import fileinput
import tempfile
from random import choice
import glob, shutil

from fabric.version import VERSION
if VERSION < (0, 9, 3, "final", 0):
    warn("Fabric < 0.9.3: Check argument order of fabric.contrib.files.contains(...)")

env.python_version = '2.7'
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

OVERWRITE = 0
MERGE = 1
KEEP = 2

def _check_exists_skip(path):
    if os.path.exists(path):
        answer = prompt('Path %s already exists. Overwrite [o], merge [m] or keep [k]? ' % path, default='k')
        if answer == 'o':
            local("rm -rf '%s'" % path)
            return OVERWRITE
        elif answer == 'm':
            warn("merge into '%s'" % path)         
            return MERGE   
        else:
            warn('skip step')
            return KEEP
    return OVERWRITE

def _create_from_template(root_path, templates):
    
    def _copy_file(template, dirpath, template_path):
        if len(template) > 2 and type(template[2]) == str:
            dirpath = os.path.join(dirpath, template[2])
        local("cp -r %s %s" % (template_path , dirpath))

        if os.path.splitext( template_path )[-1] == '.sh':
            local("chmod +x %s" % os.path.join(dirpath, template[-1]))
             
    local("mkdir -p %s" % root_path)
    
    for template in templates:
        if os.path.isdir(os.path.join(env.template_folder,template[0])):
            dirpath = root_path
        else:
            dirpath = os.path.join(root_path, template[0])
            if template[0]:
                local("mkdir -p %s" % dirpath)
         
        if len(template) > 1 and template[1]:
            template_path = os.path.join(env.template_folder,template[1])
        elif len(template) == 1:
            template_path = os.path.join(env.template_folder,template[0])
        else:
            return
             
        if os.path.exists(template_path):
           _copy_file(template, dirpath, template_path) 

        
        elif len(template) > 1:
            search_path = os.path.join(env.template_folder, template[1].split('.')[-1], template[1])
            if os.path.exists(search_path):                
                _copy_file(template, dirpath, search_path)
            
            local("touch %s" % (os.path.join(dirpath,template[1])))
            
        if type(template[-1]) == dict:
            _replace_dict(dirpath, template[-1])

def _exec_mngmt_command(command, path='%(projectpath)s/src/%(projectname)s', manage_py='python manage.py'):
    
    #s = '/bin/bash -c " cd %(projectpath)s/src/%(projectname)s && source %(projectenvpath)s/bin/activate && django-admin.py '+command+'"'
    s = '/bin/bash -c "cd '+path+' && source %(projectenvpath)s/bin/activate && '+manage_py+' '+command+' --settings=%(projectname)s.settings "'
    print local(s % env)

def _replace_dict(path, replace_dict):
    
        def _replace_in_files(arg, dirname, names):
            for name in names:
                filepath =  os.path.join(dirname, name)            
                if os.path.isfile(filepath):
                    for line in fileinput.input(filepath,inplace=1):
                        for key, value in replace_dict.items():
                            line = line.replace("{{%s}}" % key, value)
                        sys.stdout.write(line)
        
        os.path.walk(path, _replace_in_files, None)    

SRC_TEMPLATE = [
    ('media/', '.keep'),
    ('', 'settings_local.py', {'logpath':'', 'debug': 'True'}),
    ('', 'settings_local.py', 'settings_local.example.py', {'logpath':'', 'debug': 'True'}),
    ('', 'urls.py'),    
    ('', 'settings.py'),     
    ('', 'wsgi.py'),    
    ('', 'runserver.sh'),    
    ('external_fixtures/',),
]

CORE_TEMPLATE = [
    ('static/',),
    ('templates/',),
    ('', 'core_urls.py', 'urls.py'),
    ('', 'views.py'),  
]

def twitter_bootstrap(projectpath):
    _setlocal_env(projectpath)
    tmpdir = tempfile.mkdtemp()
    
    def _download_extract(url, filename):
        
        import zipfile
        import urllib
        
        topath = os.path.join(tmpdir,filename)
        print 'Download file %s to %s' % (url, topath)
        urllib.urlretrieve(url, topath)
        
        
        extract_dir = os.path.join(tmpdir, '%s.dir' % filename)
        print 'Extract file %s to %s' % (filename, extract_dir)
        
        zf = zipfile.ZipFile(topath, 'r')
        zf.extractall(os.path.join(tmpdir, extract_dir))
        
        return os.path.join(extract_dir, os.listdir(extract_dir)[0])

    def _copy_from(extract_dir, template):
        for frompath, mask, topath in template:
            files = glob.iglob(os.path.join(extract_dir, frompath, mask))
            for file in files:
                if os.path.isfile(file):
                    shutil.copy2(file, topath)
   
    #handle botstrap
    sass_extract_dir = _download_extract('https://github.com/jlong/sass-twitter-bootstrap/zipball/master', 
                      'sass-twitter-bootstrap.zip')

    SASS_TEMPLATE = [
        ('lib/','*.scss', os.path.join(projectpath, 'compass','config','sass')),
        ('img/','*.*', os.path.join(projectpath,'src', env.projectname, 'core', 'static', 'img')),
        #('js/','*.js', os.path.join(projectpath,'src', env.projectname, 'core', 'static', 'js', 'libs')),
    ]
    
    print 'copy sass-twitter-bootstrap files..'
    _copy_from(sass_extract_dir, SASS_TEMPLATE)
    
    bootstrap_extract_dir = _download_extract('http://twitter.github.com/bootstrap/assets/bootstrap.zip',
                      'bootstrap.zip')

    BOOTSTRAP_TEMPLATE = [
        ('js/','*.js', os.path.join(projectpath,'src', env.projectname, 'core', 'static', 'js', 'libs')),
    ]
    print 'copy bootstrap files..'

    _copy_from(bootstrap_extract_dir, BOOTSTRAP_TEMPLATE)
    
    shutil.rmtree(tmpdir)

def bootstrap(projectpath):

    _setlocal_env(projectpath)

    PROJECT_TEMPLATE = [         
        ('env/',),
        ('compass/',),
        ('src',),
        ('log', '.keep'),
        ('env/stage', 'settings_local.py', {'logpath': '/srv/www/'+env.projectname+'/stage/log/', 'debug': 'False'}),
        ('env/prod', 'settings_local.py', {'logpath': '/srv/www/'+env.projectname+'/prod/log/', 'debug': 'False'}),
        ('env/stage', 'nginx.conf', {'env':'stage'}),
        ('env/prod', 'nginx.conf', {'env':'prod'}),    
        ('', 'README.rst'),
        ('src/db', '.keep'),   
        ('', '.gitignore')    
    ]
 
    skip_project = _check_exists_skip(projectpath)
    
    if skip_project in (OVERWRITE, MERGE):
        _create_from_template(projectpath, PROJECT_TEMPLATE)
    
    virtualenv(projectpath)
        
    if skip_project in (OVERWRITE, MERGE):
        
        if skip_project == OVERWRITE:
            _exec_mngmt_command('startproject %(projectname)s', path='%(projectpath)s/src/', manage_py='django-admin.py')
        _create_from_template(os.path.join(projectpath,'src', env.projectname), SRC_TEMPLATE)
           
        replace_dict = {'projectpath': env.projectpath, 'projectname': env.projectname, 
                        'parentfolder': env.parentfolder, 'projectenvpath': env.projectenvpath,
                        'projectsecret': ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])}
        
        _replace_dict(env.projectpath, replace_dict)
        
        if skip_project == OVERWRITE:
            _exec_mngmt_command('startapp core')
        _create_from_template(os.path.join(projectpath,'src', env.projectname, 'core'), CORE_TEMPLATE)
        
        _replace_dict(env.projectpath, replace_dict)
        
        twitter_bootstrap(projectpath)
        
        _exec_mngmt_command('resetload')

        _add_config_dict = {}
        def _add_config(replace_var, question):
            answer = prompt(question, default='<none>')
            if answer <> '<none>':
                _add_config_dict[replace_var] = answer

        _add_config('server', 'Servername?')
        _add_config('python_version', 'Python version server?')
            
        _replace_dict(env.projectpath, _add_config_dict)   

        local('chmod +x %s' % os.path.join(projectpath,'src', env.projectname, 'runserver.sh'))
        
        print '\nAttention: Run runserver.sh to compile CSS files!'
          

def virtualenv(projectpath):
    _setlocal_env(projectpath)
    if _check_exists_skip(env.projectenvpath) in (0,1):
        print local("virtualenv --no-site-packages  --python=python%(python_version)s %(projectenvpath)s" % env)
        pip(projectpath)

def pip(projectpath):
    
    def _install_pip_file(pip_file):
        print local('/bin/bash -c "source %s/bin/activate '
              '&& pip install pip'
              ' && pip install -r %s/env/%s"' % (env.projectenvpath, pip_path, pip_file))
    
    _setlocal_env(projectpath)
    if os.path.exists(env.projectpath):
        pip_path = env.projectpath
    else:
        pip_path = env.template_folder

    _install_pip_file('dev.pip')    
    _install_pip_file('req.pip')
