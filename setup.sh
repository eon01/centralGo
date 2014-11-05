#!/usr/bin/env bash
cat README.md

if [ -d "/opt/CentralGo/" ];then
        echo -e "\n=== ERROR === \n A directory called CentralGo already exists in /opt/"
        exit
fi

mkdir /opt/CentralGo/

cp * /opt/CentralGo/
if [ $? -eq 0 ];then
        echo -e "\n=== ERROR === \n Cannot copy files to /opt/CentralGo, please consider copying them manually"
        exit
fi


ln -s /opt/CentralGo/centralgo.py /usr/bin/centralgo
if [ $? -eq 0 ];then
        echo -e "\n=== ERROR === \n ln -s /opt/CentralGo/centralgo.py /usr/bin/centralgo \ncannot be executed"
        exit
fi
