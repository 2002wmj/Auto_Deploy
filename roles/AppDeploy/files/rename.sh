#!/bin/bash
#mv -f ./app_tar/*.tar.gz ./app_tar/old_tar/
find . -maxdepth 1 -type f -name "*.tar.gz"|
while read name; do
na=$(echo $name | awk -F "-" '{{print $1"-"$2"-"$3".tar.gz"}}')
if [[ $name != $na ]]; then
mv -f ./app_tar/$na ./app_tar/old_tar/
mv "$name" $na
fi
done
mv -f *.tar.gz ./app_tar
