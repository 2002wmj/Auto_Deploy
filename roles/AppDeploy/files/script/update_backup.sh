#!/bin/bash
#升级APP前先在本地进行备份的脚本
BACKUP_DIR="/home/app_backup/"
APP_NAME=$1
APP_GROUP=$2
APP_DIR="gigold-$2-$1"


if [ ! -d "/data/deploy/$APP_DIR/ROOT" ];
then
echo "The $APP_NAME app directory does not exist"
exit 1
fi

if [ ! -d "$BACKUP_DIR/$APP_DIR" ];
then
echo "Create backup directory"
mkdir -p "$BACKUP_DIR/$APP_DIR"
fi

echo "Start backup $APP_NAME app directory."
cd "$BACKUP_DIR"
rm -rf "$BACKUP_DIR/$APP_DIR/ROOT"
cp -ar "/data/deploy/$APP_DIR/ROOT" "$BACKUP_DIR/$APP_DIR/" && tar -czf "$APP_DIR.tar.gz" "$APP_DIR/"
