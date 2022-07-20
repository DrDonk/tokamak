#!/usr/bin/env zsh
#set -x
vmnet-cli --stop
rm -rfv /Library/Preferences/VMware\ Fusion/vmnet1
rm -fv /var/db/vmware/vmnet-dhcpd-vmnet1.leases
rm -fv /var/db/vmware/vmnet-dhcpd-vmnet1.leases~
rm -rfv /Library/Preferences/VMware\ Fusion/vmnet8
rm -fv /var/db/vmware/vmnet-dhcpd-vmnet8.leases
rm -fv /var/db/vmware/vmnet-dhcpd-vmnet8.leases~
rm -fv /var/log/vnetlib 
cp -fv networking /Library/Preferences/VMware\ Fusion/networking
/Applications/VMware\ Fusion.app/Contents/Library/vmnet-cli --configure
/Applications/VMware\ Fusion.app/Contents/Library/vmnet-cfgcli enumdhcpmac2ip vmnet8
/Applications/VMware\ Fusion.app/Contents/Library/vmnet-cfgcli enumportfwd vmnet8 tcp
/Applications/VMware\ Fusion.app/Contents/Library/vmnet-cli --start
/Applications/VMware\ Fusion.app/Contents/Library/vmnet-cli --status
