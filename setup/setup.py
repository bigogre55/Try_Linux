#!/usr/bin/env python

from os import system,path,listdir,geteuid
from shutil import move,copy
import subprocess
import sys

def space(n):
  for i in range(n):
    print ""

def sudo_check():
  if geteuid() == 0:
    print "We're Root!"
    print "Moving on..."
  else:
    print("We're not Root")
    subprocess.call(['/usr/bin/sudo', './setup.py'])
    exit(1)


#system('clear')
space(1)
print "This is the setup program for Try_Linux!"
space(1)
print "	This setup program needs root access to install"
print "	and setup all necissary files."
print "	I will be check for admin privileges now."
space(2)
raw_input("Press Enter to continue.")
sudo_check()
#system('clear')
print "Checking dependencies..."
virt = system('which virsh')
php = system('which php')
print virt
print php
if virt == "" or php == "":
  space(5)
  print "	Dependency Check failed!"
  space(2)
  print "	Please make sure libvirt and PHP7.0 are installed"
  space(2)
  exit(1)
else:
  space(5)
  print "	Check Passed! Moving on"
space(1)
raw_input("Press Enter when you're ready to begin!")
#system('clear')
space(5)
print "	The VM storage pool is where the images that libvirt"
print "	creates. If you are unsure run the command:"
print "		$: virsh pool-list"
print "	This will list the current storage pools. If there is"
print "	only one run the following command and replace <pool>"
print "	with the name of the storage pool"
print "		$: virsh pool-xmldump <pool> | grep path"
print "	This will output the path to the storage pool. You"
print "	can copy and paste it here."
space(1)
vm_space = raw_input("Where is your VM storage pool: ")
exist_check = path.exists(vm_space)
dir_check = path.isdir(vm_space)
if exist_check == False:
  space(2)
  print "	That directory does not exist."
  space(2)
  exit(1)
elif dir_check == False:
  space(2)
  print "	That is not a directory"
  space(2)
  exit(1)
print "Making Directory stucture"
print vm_space[len(vm_space) - 1]
if vm_space[len(vm_space) - 1] != "/":
  vm_space += "/"
if not path.isdir(vm_space + '../config.d'):
  system('sudo mkdir ' + vm_space + '../config.d')
if not path.isdir(vm_space + '../MID'):
  system('sudo mkdir ' + vm_space + '../MID')
raw_input('Completed Sucsessfully! Press Enter to continue')
if not path.exists(vm_space + '../recycle.sh'):
  copy('../vm_space/recycle.sh', vm_space + '../')
crontab = open("/etc/crontab","r")
crontab = crontab.read()
count = 0
for line in crontab:
  count = count + 1
  pre = str(count) + " " + str(line)
  print pre
  print '\n'

with open("/etc/crontab", "a") as cron:
  cron.write("\n")
  cron.write("*/15 * * * * root /bin/rm -f /srv/storage/virtual_machines/config.d/*" + "\n")
  cron.write("*/5 * * * * root /srv/storage/virtual_machines/recycle.sh" + "\n")

#system('clear')
space(2)
print "	all done"
space(2)

