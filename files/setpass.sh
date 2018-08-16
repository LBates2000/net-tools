#!/bin/bash
SB_PW=$(curl 172.17.0.1:2330/v1/infospace/shellinabox | jq -r '.value')
export SB_PW

# If value is null then default password will be used
if [ -n "$SB_PW" ]
then
	echo cloudops:${SB_PW} | chpasswd
fi

unset -v SB_PW
