#!/bin/bash
name=$1
dist=$2
/usr/bin/virsh vol-clone $dist.img $name.img --pool base_images > /dev/null 2>&1

