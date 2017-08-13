#!/usr/bin/env python

from os import system

print "This is the setup program for Try_Linux!"
print ""
raw_input("Press Enter to continue.")
system('clear')
print "Checking dependencies..."
virt = system('which virsh')
phpv = system('which php')
if virt == "" or phpv == "":
  print ""
  print "Dependency Check failed!"
  print ""
  print "Please make sure libvirt and PHP7.0 are installed"
  exit(1)
else:
  print ""
  print "Check Passed! Moving on"
print "	The VM storage pool is where the images that libvirt"
print "	creates. If you are unsure run the command:"
print "		$: virsh pool-list"
print "	This will list the current storage pools. If there is"
print "	only one run the following command and replace <pool>"
print "	with the name of the storage pool"
print "		$: virsh pool-xmldump <pool> | grep path"
print "	This will output the path to the storage pool. You"
print "	can copy and paste it here."
print ""
raw_input("press enter when ready.")
vm_space = raw_input("Where is your VM storage pool: ")
print "Making Directory stucture"
raw_input()
system('clear')
print "all done"

