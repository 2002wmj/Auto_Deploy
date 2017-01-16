#!/bin/bash
#使用本地备份对APP进行升级回滚操作脚本
BACKUP_DIR="/home/app_backup/"
APP_NAME=$1
APP_GROUP=$2
PRO_NAME=$3
APP_DIR="$3-$2-$1"


if [ ! -d "/data/deploy/$APP_DIR/ROOT" ] || [ ! -d "$BACKUP_DIR/$APP_DIR/ROOT" ];
then
echo "The $APP_NAME installation directory or the backup file does not exist!"
exit 1
fi

echo "Start rolling back $APP_NAME app."
rm -rf "/data/deploy/$APP_DIR/ROOT" && cp -ar "$BACKUP_DIR/$APP_DIR/ROOT" "/data/deploy/$APP_DIR/ROOT"
chown -R oper:oper /data/deploy && chmod -R g-w /data/deploy
rm -f "/root/$APP_DIR.tar.gz"
