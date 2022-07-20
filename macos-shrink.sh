#!/usr/bin/env bash
dd if=/dev/zero of=zerofile bs=16m count=1000000
sync
rm zerofile
/Library/Application\ Support/VMware\ Tools/vmware-tools-daemon --cmd='disk.shrink'
