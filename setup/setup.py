#!/usr/bin/env python3

from os import system,path,listdir,geteuid
from shutil import move,copy,copytree
import gzip
import subprocess
import sys
import urllib.request

def space(n):
  for i in range(n):
    print("")

def sudo_check():
  if geteuid() == 0:
    print("We're Root!")
    print("Moving on...")
  else:
    print("We're not Root")
    subprocess.call(['/usr/bin/sudo', './setup.py'])
    exit(1)

def get_img():
  print('Downloading CentOS base image..')
  web = urllib.request.urlopen('https://s3-us-west-2.amazonaws.com/jacobjeffers/git/TryLinux_centos.img.gz')
  deb_img = web.read()
  with open(vm_space + 'TryLinux_centos.img.gz', 'wb') as file:
    file.write(deb_img)
  print('image has been downloaded; checking integrity..  ')
  check_img()
  print('Extracting image..   ')
  extract_img()

def check_img():
  import hashlib
  new_md5 = hashlib.md5(open(vm_space + 'TryLinux_centos.img.gz', 'rb').read()).hexdigest()
  new_md5 = str(new_md5)
  old_md5 = 'f3e3bd285dbc727848991917e2e9a8c1'
#  print(new_md5)
#  print(old_md5)
  if old_md5 == new_md5:
    print('The image is good')
  else:
    print('The image did not download correctly; Trying again')
    system('rm -f ' + vmspace + 'TryLinux_centos.img.gz')
    get_img()

def extract_img():
  system('sudo gunzip -qf ' + vm_space + 'TryLinux_centos.img.gz')
  print('img has been extracted')
  e = pool_set()
  e = str(e)
  e = e[2:-2]
#  input('extract refresh pool is ' + e)
  system('sudo virsh pool-refresh ' + str(e)) 

def refresh_pool(l):
  system('virsh pool-refresh --pool ' + str(l))

def get_pool_name():
  vms = listdir(vm_space)
  for a in range(len(vms)):
#    input('get_pool_name last 4 are ' + vms[a][-4:])
    if vms[a][-4:] == '.img':
      responce = subprocess.check_output('sudo virsh vol-pool ' + vm_space + vms[a], shell=True)
      responce = str(responce)
      responce = responce[2:-5]
  return responce

def get_storage_pool_info():
  vm_space = input("Where is your VM storage pool: ")
  exist_check = path.exists(vm_space)
  dir_check = path.isdir(vm_space)
  if exist_check == False:
    space(2)
    print("	That directory does not exist.")
    space(2)
    exit(1)
  elif dir_check == False:
    space(2)
    print("	That is not a directory")
    space(2)
    exit(1)
  else:
    print("	OK!!")
    return(vm_space)

def pool_list_fix(old):
  i = 4
#  print('first new is ' + str(new))
  global new
  if not i >= len(old):
    new = []
    for a in range(len(old) - 1):
      if old[i][-2:] == "\n\n":
        break
    new.append(old[i])
    i = i + 3
#  print('new in fix is ' + str(new))
#  input()
  return new

def pool_set():
  pools = []
  import re
  responce = subprocess.check_output('virsh pool-list', shell=True)
  responce = responce.decode().split(" ")
  for field in responce:
    if len(field) > 1:
      pools.append(field)
#  print('pools in pool_set are ' + str(pools))
#  input()
  pool_list = pool_list_fix(pools)
  return pool_list

def auto_get_pool_info(w):
  pool_list = []
  pools = pool_set()
#  if pools[len(pools) - 1] == '\n-------------------------------------------\n\n':
  if not pools:
    print('there are no storage pools; creating one..')
    vm_space = build_pool()
  pools = pool_set()
  pool_list = pool_list_fix(pools)
#  print(pool_list)
#  input()
  if len(pool_list) > 1:
    print('There is more than one storage pool: ')
    for i in range(len(pool_list)):
      a = i + 1
      print(str(a) + ": " + pool_list[i])
    c = input('Which one Should I use:')
    c = int(c) - 1
    pool = str(pool_list[c])
  elif len(pool_list) == 1:
    pool = pool_list
    pool = str(pool)
    pool = pool[2:-2]
  responce = subprocess.check_output('virsh pool-dumpxml --pool ' + pool + ' | grep path', shell = True)
  responce = str(responce)
  vm_space = responce[12:-10]
  if w == 'pool':
    return(pool)
  elif w == 'vm_space':
    return(vm_space)
  else:
    print('bad call to auto_get_pool_info(). need to specify what var to retrieve. vm_space or pool')

def build_pool():
  subprocess.call(['sudo','virsh','pool-define','../vm_space/new_pool.xml'])
  subprocess.call(['sudo','virsh','pool-start','TryLinux_images'])
  subprocess.call(['sudo','virsh','pool-autostart','TryLinux_images'])


def install_dep():
  subprocess.call(['sudo','apt','-y','install','php7.0','libvirt-bin','qemu-kvm','virtinst','bridge-utils','cpu-checker'])

def build_vars():
  if not path.exists('../web/vars.php'):
    print("Creating vars file")
    system('touch ../web/vars.php')
    with open("../web/vars.php", "w") as vars:
      vars.write("<?php\n")
      vars.write("//the directory for the virtual machine storage\n")
      vars.write('$dir = \"' + vm_space + '\";\n')
      vars.write("?>\n")
  else:
    print("vars file is present")

def build_start(pool):
  if not path.exists('../web/start.sh'):
    print("Creating start file")
    system('touch ../web/start.sh')
    with open("../web/start.sh", "w") as start:
      start.write('#!/bin/bash\n')
      start.write('name=$1\n')
      start.write('dist=$2\n')
      start.write('/usr/bin/virsh vol-clone $dist.img $name.img --pool ' + pool + ' > /dev/null 2>&1\n')
  else:
    print("start file is present")

new = []
#system('clear')
space(1)
print("This is the setup program for Try_Linux!")
space(1)
print("	This setup program needs root access to install")
print("	and setup all necissary files.")
print("	I will be check for admin privileges now.")
space(2)
input("Press Enter to continue.")
sudo_check()
#system('clear')
print("Checking dependencies...")
dep = 0
install = False
while(dep < 1):
  virt = system('which virsh')
  php = system('which php')
  if virt > 0 or php > 0:
    space(5)
    print("	Dependency Check failed!")
    space(2)
    print("	Please make sure libvirt and PHP7.0 are installed")
    space(2)
    install = input('Do you want me to install Libvirt and PHP?(y/n) ')
    if install == "y" or install == "Y":
      install_dep()
      dep = dep + 1
  else:
    space(5)
    print("	Check Passed! Moving on")
    dep = dep + 1
space(1)
input("Press Enter when you're ready to begin!")
#system('clear')
space(5)
if install == False:
  print("	The VM storage pool is where the images that libvirt")
  print("	creates. If you are unsure run the command:")
  print("		$: virsh pool-list")
  print("	This will list the current storage pools. If there is")
  print("	only one run the following command and replace <pool>")
  print("	with the name of the storage pool")
  print("		$: virsh pool-xmldump <pool> | grep path")
  print("	This will output the path to the storage pool. You")
  print("	can copy and paste it here.")
  space(1)
  vm_space = get_storage_pool_info()
else:
  vm_space = auto_get_pool_info('vm_space')
print("Making Directory stucture and installing files")
if vm_space[len(vm_space) - 1] != "/":
  vm_space += "/"
if not path.isdir(vm_space + '.Try_Linux/config.d'):
  system('sudo mkdir -p ' + vm_space + '.Try_Linux/config.d')
  print("Creating config.d directory")
else:
  print("config.d dir is present")
if not path.isdir(vm_space + '.Try_Linux/MID'):
  system('sudo mkdir -p ' + vm_space + '.Try_Linux/MID')
  print("Creating MID directory")
else:
  print("MID dir is present")

if not path.exists(vm_space + '.Try_Linux/recycle.sh'):
  copy('../vm_space/recycle.sh', vm_space + '.Try_Linux/')
  print("Copying recycle.sh to " + vm_space + '.Try_Linux/')
else:
  print("recycle.sh is present")

#make folder permissions
if path.isdir(vm_space + '.Try_Linux'):
  system('sudo chmod 777 ' + vm_space + '.Try_Linux')
if path.isdir(vm_space + '.Try_Linux/MID'):
  system('sudo chmod 777 ' + vm_space + '.Try_Linux/MID')
if path.isdir(vm_space + '.Try_Linux/config.d'):
  system('sudo chmod 777 ' + vm_space + '.Try_Linux/config.d')
if path.exists(vm_space + '.Try_Linux/recycle.sh'):
  system('sudo chmod 777 ' + vm_space + '.Try_Linux/recycle.sh')

if not path.exists('/etc/cron.d/Try_Linux'):
  print("Creating cron file")
  system('touch /etc/cron.d/Try_Linux')
  with open("/etc/cron.d/Try_Linux", "w") as cron:
    cron.write("#-------------------------------------------------------#")
    cron.write("#Try_Linux cleanup for virtual machines and config files#")
    cron.write("#-------------------------------------------------------#")
    cron.write("\n")
    cron.write("*/15 * * * * root /bin/rm -f /srv/storage/virtual_machines/config.d/*" + "\n")
    cron.write("*/5 * * * * root /srv/storage/virtual_machines/recycle.sh" + "\n")
else:
  print("cron file is present")
#system('clear')
input('Completed Sucsessfully! Press Enter to continue')
space(2)
refresh_now = True #testing without Download
vm_list = listdir(vm_space)
if vm_list == []:
  print("You have no base images!")
  print("Moving base CentOS image to " + vm_space)
  get_img()
  refresh_now = True
else:
  print("your current virtual machines are:")
  for i in range(len(vm_list)):
    if not vm_list[i][0] == ".":
      print(vm_list[i])
  download = input('Do you want to download the CentOS image?(y/n) ')
  if download == 'yes' or download == 'y' or download == "Y":
    get_img()
    refresh_now = True

if refresh_now == True:
  r = get_pool_name()
#  print('r is ' + str(r))
  refresh_pool(r)

build_vars()
build_start(r)

webdir = input('Where is your Web folder: ')
if not path.exists(webdir + 'Try_Linux'):
  system('sudo mkdir -p ' + webdir + 'Try_Linux')
  system('sudo cp -ru ../web/* ' + webdir + 'Try_Linux/')
  system('sudo chmod 777 ' + webdir + 'Try_Linux/*')

system('sudo chmod 777 ' + vm_space)
system('sudo chmod 777 ' + vm_space + '.Try_Linux')
system('sudo chmod 777 ' + vm_space + '.Try_Linux/*')

space(2)
print("	all done")
space(2)

