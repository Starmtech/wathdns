#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
import shutil

#if _platform == "linux" or _platform == "linux2":
   # linux
#elif _platform == "darwin":
#   print 'aucune version compatible pour le moment'
#elif _platform == "win32":
#   print 'aucune version compatible pour le moment'
#elif _platform == "win64":
#   print 'aucune version compatible pour le moment'

print 'installation de python-dnspython'
apt install python-dnspython

print 'installation de libsqlite3-dev'
apt install libsqlite3-dev

PATH = os.path.dirname(os.path.abspath(__file__))
if os.path.isdir('/opt/wathdns') == False:
   os.makedirs('/opt/wathdns')
   print "Création du dossier wathdns dans /opt"
else:
   print "Le dossier existe déjà"
shutil.copyfile(PATH+'/wathdns.py', "/opt/wathdns/wathdns.py")
print "Déplacement du fichier dans /opt/wathdns/"
shutil.copyfile(PATH+'/wathdns.db', "/opt/wathdns/wathdns.db")
print "Déplacement de la base de donnée dans /opt/wathdns/"
print '\n'
try:
   os.symlink('/opt/wathdns/wathdns.py','/usr/local/bin/wathdns')
   print "Création du liens symbolique"
except OSError:
   print 'le fichier existe'
   pass

print '\n'
os.chmod("/usr/local/bin/wathdns", 0755)
print 'Droit modifier sur wathdns.py'
print 'fin'
