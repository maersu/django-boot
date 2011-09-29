{{projectname}}
==============================================================================

Compass/SASS
-------------
```
sudo apt-get install ruby-dev ruby
gems compass rb-inotify
```

Add /var/lib/gems/1.8/bin to PATH
More information: http://compass-style.org http://sass-lang.com

Virtualenv
----------

activate env
************
```
source {{projectname}}-env/bin/activate
```

get and install packages (or update)
************************************
```
source {{projectname}}-env/bin/activate
pip install pip pyinotify
pip install -r dependencies.pip
pip install -r req.pip
pip install -r dev.pip
```

deactivate env
**************
```
deactivate
```

uninstall a package
*******************

`pip -E {{projectname}}-env/ uninstall <PACKAGE_NAME>`

.bashrc
-------
```
cd() {
  builtin cd $@
  pwd | egrep -q '{{parentfolder}}/.+' \
  && source ~/{{parentfolder}}/`pwd | sed -r 's@^.*{{parentfolder}}/([^/]+).*$@\\1@'`-env/bin/activate \
  || { type deactivate &>/dev/null && deactivate; }
}

```

Eclipse: Configure Python Interpreter
-------------------------------------
Under Preferences > Pydev > Interpreter - Python add a new interpreter named `{{projectname}}` 
and choose `{{projectname}}-env/bin/python` as the Interpreter Executable.

Hosts File
----------
```
sudo vim /etc/hosts

127.0.0.1       app.dev
```

