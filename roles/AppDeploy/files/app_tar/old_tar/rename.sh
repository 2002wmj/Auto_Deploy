#!/bin/bash
find . -maxdepth 1 -type f -name "*.tar.gz"|
while read name; do
na=$(echo $name | awk -F "-" '{{print $1"-"$2"-"$3".tar.gz"}}')
if [[ $name != $na ]]; then
mv "$name" $na
fi
done
#mv *.tar.gz ./app_tar
