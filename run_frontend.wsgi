#coding:utf-8
import os
import sys
import site
#add site-packages of the chosen virtualenv to work with
site.addsitedir('/home/fp862/.virtualenvs/env_showoff/lib/python2.7/site-packages')

#add app's directory to the PYTHONPATH
sys.path.append("/var/www/showoff")

#activate virtual env
activate_env=os.path.expanduser("/home/fp862/.virtualenvs/env_showoff/bin/activate_this.py")
execfile(activate_env,dict(__file__=activate_env))

from run_frontend import app as application
