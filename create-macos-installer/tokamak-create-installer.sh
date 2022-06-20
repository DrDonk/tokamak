#!/bin/bash

# Based on this script https://github.com/rtrouton/create_macos_vm_install_dmg/blob/main/create_macos_vm_install_dmg.sh

set -x

usage() {
	cat <<HELP
Usage:
$(basename "$0") "/path/to/Install macOS [Name].app" /path/to/output/directory

Description:
This script uses a macOS 10.12 and later installer application to create a .dmg disk image file suitable for use
with virtualization software like VMware or Parallels. The .dmg disk image file will be named as follows:

macOS_[OS Version Number Here]_installer.dmg.

Optional:

Script can also create a .iso disk image file. The .iso disk image file will be named as follows:

macOS_[OS Version Number Here]_installer.iso.

Requirements:

Compatible macOS installer application
Account with the ability to run commands using sudo, to allow specific functions to run with root privileges.

HELP
}

# Provide custom colors in Terminal for status and error messages

msg_status() {
	echo -e "\033[0;32m-- $1\033[0m"
}
msg_error() {
	echo -e "\033[0;31m-- $1\033[0m"
}

admin_check() {
    # Check that the script is being run by an account with admin rights
    if [[ -z $(id -nG | grep -ow admin) ]]; then
        msg_error "This script will need to use sudo to run specific functions" 
        msg_error "using root privileges. The $(id -nu) account does not have"
        msg_error "administrator rights associated with it, so it will not be"
        msg_error "able to use sudo."
        echo ""
        msg_error "Script will now exit."
        msg_error "Please try running this script again using an admin account."
        echo ""
        exit 4 # Running as standard account without sudo rights.
    fi
}

admin_check

# Script will prompt user if they want an additional image in .iso format.

# echo "Do you also want an .iso disk image?"
# select yn in "Yes" "No"; do
# 	case $yn in
# 		Yes) ISO=1; msg_status "Additional disk image will be created in .iso format. Proceeding..."; break;;
# 		No) msg_status "Additional disk image will not be created in .iso format. Proceeding..."; break;;
# 	esac
# done

install_esd="$1"

if [[ -z "$1" ]] || [[ ! -d "$1" ]]; then
    msg_error "The path to the macOS installer application is required as the first argument."
    usage
	exit 1
fi

if [[ -z "$2" ]] || [[ ! -d "$2" ]]; then
    msg_error "An output directory is required as the second argument."
    usage
	exit 1
else
	output_directory="$2"
fi

# Remove trailing slashes from input paths if needed

install_esd=${install_esd%%/}
output_directory=${output_directory%%/}

macOS11=0

if [[ -d "$install_esd" ]] && [[ -e "$install_esd/Contents/SharedSupport/InstallESD.dmg" ]]; then
   msg_status "macOS Installer application detected at the following path: $install_esd"
elif [[ -d "$install_esd" ]] && [[ ! -e "$install_esd/Contents/SharedSupport/InstallESD.dmg" ]] && [[ -e "$install_esd/Contents/SharedSupport/SharedSupport.dmg" ]]; then
   msg_status "macOS Installer application detected at the following path: $install_esd"
   macOS11=1
else
   msg_error "macOS Installer application not detected."
   usage
   exit 1
fi

if [[ "$macOS11" = 1 ]]; then
    hdiutil attach "$install_esd/Contents/SharedSupport/SharedSupport.dmg" -quiet -noverify -mountpoint "/Volumes/Shared Support"
    installer_version=$(/usr/libexec/PlistBuddy -c 'Print :Assets:0:OSVersion' "/Volumes/Shared Support/com_apple_MobileAsset_MacSoftwareUpdate/com_apple_MobileAsset_MacSoftwareUpdate.xml")
    hdiutil detach "/Volumes/Shared Support"* -force -quiet   
else
    installer_version=$(/usr/libexec/PlistBuddy -c 'Print :System\ Image\ Info:version' "$install_esd/Contents/SharedSupport/InstallInfo.plist")
fi
installer_version_digits_only=$(echo $installer_version | awk -F'[^0-9]*' '$0=$1$2$3' | sed 's/^[0-9]\{3\}$/&0/')
installer_qualifies=$(echo $installer_version_digits_only | head -c4)
random_disk_image_name=$(uuidgen)
installer_mounted_volume=$(echo "$install_esd" | grep -o 'Install.*' | sed 's/....$//')
installer_name=$(echo macOS_"$installer_version_digits_only"_installer)

if [[ "$installer_qualifies" -lt 1012 ]]; then
    msg_error "This script supports building installer disk image files for macOS 10.12.0 and later."
    msg_error "Please use an installer app which installs macOS 10.12.0 or later."
    usage
	exit 1
else
    msg_status "Installer application for macOS $installer_version detected. Proceeding...."
fi

if [[ -x "$install_esd/Contents/Resources/createinstallmedia" ]]; then
   msg_status "$install_esd/Contents/Resources/createinstallmedia tool detected. Proceeding...."
else
   msg_error "The createinstallmedia tool from $install_esd/Contents/Resources is not executable or is missing!" 
   msg_error "This macOS installer application may not be complete or working properly."
   exit 1
fi

# Creating a temporary disk image in $output_directory and mounting it. 
# For maximum compatibility, the file system on the disk image is set to use
# Journaled HFS+.

if [[ "$macOS11" = 1 ]]; then
	# Check if 12+ as Monterey needs bigger DMG 
	if [["$installer_qualifies" -lt 1200 ]]; then
    	disk_image_size=13
    else
        disk_image_size=19
    fi
else
    disk_image_size=8
fi

disk_image_filesystem="HFS+J"

msg_status "Creating empty $disk_image_size GB disk image at the following location: $output_directory/$installer_name.dmg"
hdiutil create -o "$output_directory"/"$installer_name".dmg -size "$disk_image_size"g -layout SPUD -fs "$disk_image_filesystem"
msg_status "Mounting disk image at /Volumes/$installer_name"
hdiutil attach "$output_directory"/"$installer_name".dmg -noverify -mountpoint /Volumes/"$installer_name"

# The createinstallmedia tool requires root privileges to run, so we'll need to request 
# the password of the logged-in user if not already running the script as root.

if [[ $EUID -ne 0 ]]; then
   msg_status "You will be prompted for your password now, to run commands with root privileges"
   msg_status "using sudo. This will allow the createinstallmedia tool to copy installer files"
   msg_status "onto /Volumes/$installer_name."
fi

# The createinstallmedia tool requires different options, depending on which OS installer's createinstallmedia tool is being used.

if [[ "$installer_qualifies" -eq "1012" ]] || [[ "$installer_qualifies" -eq "1013" ]]; then
   sudo "$install_esd/Contents/Resources/createinstallmedia" --volume /Volumes/"$installer_name" --applicationpath "$install_esd" --nointeraction
else
   sudo "$install_esd/Contents/Resources/createinstallmedia" --volume /Volumes/"$installer_name" --nointeraction
fi



# Move and rename the installer disk image to match the following standard:
#
# macOS_[OS Version Number Here]_installer

# mv "$output_directory"/"$random_disk_image_name".cdr.dmg "$output_directory"/macOS_"$installer_version_digits_only"_installer.dmg

# Clean up mounted drives

msg_status "Unmounting macOS installer disk image."

for volume in "/Volumes/$installer_mounted_volume"*; do
	sudo hdiutil detach "$volume" -force -quiet
done

if [[ -e "/Volumes/Shared Support" ]]; then
   sudo hdiutil detach "/Volumes/Shared Support" -force -quiet
fi

# Create the output file name
output_dmg="$output_directory"/$installer_name.dmg

# Calculate # of 512 blocks required for flat file
byte_size="`stat -f '%z' $installer_name.dmg`"
installer_size=$((byte_size/512))

# Create the virtual disk descriptor.
cat <<VMDK >"$installer_name.vmdk"
# Disk DescriptorFile
version=1
encoding="UTF-8"
CID=fffffffe
parentCID=ffffffff
isNativeSnapshot="no"
createType="monolithicFlat"

# Extent description
RW $installer_size FLAT "$installer_name.dmg" 0

# The Disk Data Base 
#DDB

ddb.adapterType = "lsilogic"
#ddb.geometry.cylinders is not used by Mac OS.
#ddb.geometry.heads is not used by Mac OS.
#ddb.geometry.sectors is not used by Mac OS.
#ddb.longContentID will be generated on the first write to the file.
#ddb.uuid is not used by Mac OS.
ddb.virtualHWVersion = "6"
VMDK

# Check VMDK is consistent
/Applications/VMware\ Fusion.app/Contents/Library/vmware-vdiskmanager -e "$installer_name.vmdk"

# if [[ "$ISO" == 1 ]]; then
# 
#     # Convert the installer disk image to .iso format. This will create a separate copy
#     # of the installer disk image.
# 
#     msg_status "Converting macOS installer disk image to .iso format."
#     hdiutil convert "$output_directory"/macOS_"$installer_version_digits_only"_installer.dmg -format UDTO -o "$output_directory"/macOS_"$installer_version_digits_only"_installer.iso
# 
#     # Rename the converted installer disk image copy so that the filename ends in ".iso"
# 
#     mv "$output_directory"/macOS_"$installer_version_digits_only"_installer.iso.cdr "$output_directory"/macOS_"$installer_version_digits_only"_installer.iso
#     output_iso="$output_directory"/macOS_"$installer_version_digits_only"_installer.iso
# fi

# Display a message that the build process has finished and include the location of the disk image file.

msg_status "Building process complete."

if [[ -f "$output_dmg" ]]; then
  msg_status "Built .dmg disk image file is available at $output_dmg"
else
  msg_error "Build failure! Built .dmg disk image file not found!"
fi

# if [[ "$ISO" == 1 ]]; then
#   if [[ -f "$output_iso" ]]; then
#     msg_status "Built .iso disk image file is available at $output_iso"
#   else
#     msg_error "Build failure! Built .iso disk image file not found! "
#   fi 
# fi

