@echo -off
if %1 == "" then
    echo "Please pass a filename"
else
    echo "Loading %1 ..."
    dmpstore -l %1
endif
