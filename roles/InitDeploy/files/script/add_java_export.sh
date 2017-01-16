#!/bin/bash
cat << EOF >> /etc/profile
export JAVA_HOME=/usr/local/jdk1.7.0_79/
export PATH=\$JAVA_HOME/bin:\$PATH
export CLASSPATH=.:\$JAVA_HOME/lib/dt.jar:\$JAVA_HOME/lib/tools.jar
EOF
