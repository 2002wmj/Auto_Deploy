#!/bin/bash
#社区半径app升级脚本
BACKUP_DIR="/home/app_backup/"
APP_NAME=$1
APP_GROUP=$2
full_release=$3
UPGRADE=$4
APP_DIR="gigold-$2-$1"
DATE=`date +"%F  %X"`

#根据更新包大小判断是否全量发布
APP_SIZE=`du /root/$APP_DIR.tar.gz|awk '{print $1}'`
if [ $APP_SIZE -gt 10240 ];then
full_release="True"
else
full_release="False"
fi

#对app进行启动和停止操作
server_app()
{
if [ "$APP_GROUP" = "web" ];then
source /etc/profile && cd /data/deploy/$APP_DIR/apache-tomcat/bin/ && su oper -c "./tomcat.sh $1"
else
source /etc/profile && cd /data/deploy/$APP_DIR/ROOT/bin && su oper -c "./service.sh $1"
fi
if [ ! $? -eq 0 ];then
echo "$1 app server is failed!"
exit 1
fi
return 0
}

#备份app的ROOT目录
backup_app()
{
if [ ! -d "$BACKUP_DIR/$APP_DIR" ];
then
echo "Create backup directory"
mkdir -p "$BACKUP_DIR/$APP_DIR"
fi

echo "Start backup $APP_NAME app directory."
cd "$BACKUP_DIR"
rm -rf "$BACKUP_DIR/$APP_DIR/ROOT"
cp -ar "/data/deploy/$APP_DIR/ROOT" "$BACKUP_DIR/$APP_DIR/" && tar -czf "$APP_DIR.tar.gz" "$APP_DIR/"
return 0
}


#解压缩app包到指定目录
update_app()
{
if [ $full_release = "True" ]||[ $APP_GROUP = "web" ];then
rm -rf "/data/deploy/$APP_DIR/ROOT"
echo "rm deploy $APP_DIR $DATE" >>/tmp/rm_app.log
fi
tar -zxvf /root/$APP_DIR.tar.gz -C /data/deploy/ && chown -R oper:oper /data/deploy &&chmod -R g-w /data/deploy
if [ ! $? -eq 0 ];then
return 1
fi
}

#开始升级app操作
if [ -d "/data/deploy/$APP_DIR/ROOT" ];then
backup_app
fi
#判断是否升级app
if [ "$UPGRADE" = "upgrade" ];then
server_app stop
fi

update_app

#判断是否升级app
if [ "$UPGRADE" = "upgrade" ];then
server_app start
fi

#判断安装包是否正确解压
if [ ! $? -eq 0 ];then
echo "Update app is failed!"
exit 1
fi
