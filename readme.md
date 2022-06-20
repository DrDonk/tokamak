
#  Tokamak Utilities
## Introduction
Many years ago I published network configuration scripts 
(called [Tokamak](https://communities.vmware.com/t5/VMware-Fusion-Documents/Advanced-Networking-Configuration-Tokamak-Networking-Scripts-for/ta-p/2771500))
for VMware Fusion before VMware added their own network configuration utilities. I have decided to re-use 
the name for a new project with utilities and hints for VMware Fusion. The project will be quite random and contain 
scripts, code and stuff I have found useful over the years.

## Sub-projects
### OpenCore Boot Disk
There is a known problem in VMware Fusion 12, where it is not possible to boot to Recovery Mode. 
The OpenCore boot loader is capable of booting to Recovery mode which means settings such as those for SIP
can be altered.

### EFI CSR Utilities
This is an alternative to OpenCore boot disk and uses EFI shell scripts to load EFI variables from setvar DMP files.

### Create macOS Installer
An independent from VMware Fusion shell script to create a bootable VMDK from an Apple macOS Installer application. 

[TODO: Add links to wiki page]
