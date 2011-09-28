import os, sys, re, commands
from fabric.api import *
from fabric.contrib.console import *
from fabric.contrib.project import *
from fabric.contrib.files import contains, exists
from fabric.utils import warn
import xmlrpclib
import pip
from itertools import izip_longest

from fabric.version import VERSION
if VERSION < (0, 9, 3, "final", 0):
    abort("Fabric < 0.9.3: Check argument order of fabric.contrib.files.contains(...)")

# helpers
def _warning():
    warn('Accessing \x1b[5;31m%(env)s\x1b[0;39m environement' % env)
    prompt("Enter 'c' to continue", validate=r'c$')

def _local_path(*args):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), '..',  *args)

def _remote_path(*args):
    return os.path.join(env.remote_app, *args)

# environments
env.python_version = '{{python_version}}'
env.hosts = ['<some.host>']
env.local_app = _local_path('src', '{{projectname}}')
env.local_static_root = _local_path('site_media')
env.user = '<user>'
env.rsync_exclude = ['settings_local.py',
                     'settings_local.example.py',
                     '.svn/',
                     '.git/',
                     '.keep',
                     '*.pyc',
                     '{{projectname}}.dat']

REMOTE_APP_TMPL = '/home/www'

def stage():
    env.env = 'stage'
    env.remote_app = os.path.join(REMOTE_APP_TMPL, env.env)
    env.remote_virtualenv = _remote_path('{{projectname}}-env')
    env.remote_virtualenv_py = '<path/to/virtualenv.py>'
    _warning()

def prod():
    env.env = 'prod'
    env.remote_app = os.path.join(REMOTE_APP_TMPL, env.env)
    env.remote_virtualenv = _remote_path('{{projectname}}-env')
    env.remote_virtualenv_py = '<path/to/virtualenv.py>'
    _warning()

def deploy():
    require('env')
    
    check_for_updates()
    
    _ensure_virtualenv()
    # sources & templates
    rsync_project(
        remote_dir = env.remote_app,
        local_dir = env.local_app,
        exclude = env.rsync_exclude,
    )    
    run('mkdir -p %s' % _remote_path('{{projectname}}', 'public'))
    # deploy static files    
    #local('./manage.py collectstatic') # in a later iteration
    rsync_project(
        remote_dir = _remote_path('{{projectname}}', 'public'),
        local_dir = env.local_static_root,
        delete = True,
        exclude = env.rsync_exclude,
    )

    put(_local_path('env', env.env, 'settings_local.py'), _remote_path('{{projectname}}'))
    
    # deploy on alwaysdata
    #put(_local_path('env', env.env, 'django.fcgi'), _remote_path('{{projectname}}', 'public'))
    #run('chmod +x %s' % _remote_path('{{projectname}}', 'public', 'django.fcgi'))
    #put(_local_path('env', 'htaccess'), _remote_path('{{projectname}}', 'public', '.htaccess'))
    
    put(_local_path('env', 'robots.txt'), _remote_path('{{projectname}}', 'public'))
    put(_local_path('env', 'req.pip'), _remote_path())
    
    # link admin static files
    admin_media = _remote_path('{{projectname}}', 'public', 'media')
    if not exists(admin_media):
        run('ln -s %s %s' % (_remote_path('{{projectname}}-env', 
                            'src/django/django/contrib/admin/media/'),
                            admin_media))
    _update_packages()
    _clear_pycs()
    
    run('touch %s' % _remote_path('{{projectname}}', 'public', 'django.fcgi'))
    
def delete():
    if env.env != 'stage': abort("only available for 'stage'")
    run('rm -rf %s' % _remote_path('{{projectname}}'))
    run('rm -rf %(remote_virtualenv)s' % env)

def check_for_updates():
    
    def _compare_version(version_local, version_remote):
        
        status = 0
        for l, r in izip_longest(version_local.split('.'), version_remote.split('.')):
            
            if l is None:
                status = 1
                break
            elif r is None:
                status = 2
                break
            
            if l.isdigit() and r.isdigit():
                l = int(l)
                r = int(r)
            if l < r:
                status = 1
                break
            elif l > r:
                status = 2
                break

        if status == 1:
            return '\x1b[0;32m%s available\x1b[0;39m' % version_remote
        elif status == 2:
            return 'ahead (%s >= %s)' % (version_local, version_remote)
        else:
            return 'up to date'
            
    pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    print 'check for updates (local):\n'
    for dist in pip.get_installed_distributions():
        available = pypi.package_releases(dist.project_name)
        if not available:
            # Try to capitalize pkg name
            available = pypi.package_releases(dist.project_name.capitalize())
        if not available:
            # Try to lower
            available = pypi.package_releases(dist.project_name.lower())
       
        if not available:
            msg = 'no releases at pypi'
        else:
            msg = _compare_version(dist.version, available[0])
            
        pkg_info = '{dist.project_name} {dist.version}'.format(dist=dist)
        print '\t{pkg_info:40} {msg}'.format(pkg_info=pkg_info, msg=msg) 
   
def _clear_pycs():
    run("find %(remote_app)s -name '*.pyc' -print0|xargs -0 rm" % env)
    
# virtualenv targets
def _virtualenv(command):
    run("source %s/bin/activate && %s" % (env.remote_virtualenv, command))
        
def _update_packages():
    _virtualenv('pip install --upgrade pip pyinotify')
    _virtualenv('pip install -r %(remote_app)s/req.pip' % env)

def _ensure_virtualenv():
    if not exists(env.remote_virtualenv):
        run("%(remote_virtualenv_py)s --no-site-packages --python=python%(python_version)s %(remote_virtualenv)s" % env)
      
        
        