

efidisk="$( diskutil list | grep "$1" | grep "EFI" | rev | cut -d ' ' -f 1 )"
echo "$efidisk"
