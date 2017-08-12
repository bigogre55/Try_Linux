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
else:
  print ""
  print "Check Passed! Moving on"
raw_input()
system('clear')
print "all done"

