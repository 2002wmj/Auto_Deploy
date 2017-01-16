#!/bin/bash
#修改社区半径老应用Dubbo_group环境变量，并重启应用。
dubbo_group=$1
app_names=(${2//,/ })

#修改环境变量
mod_pro()
{
sed -i "s/pro.*/pro_$dubbo_group/g" /root/.bash_profile
source /root/.bash_profile
}

#重启应用服务
restart_app()
{
for app_name in ${app_names[@]}
do
/data/apps/scripts/lehome_app_cli.sh restart $app_name
if [ ! $? -eq 0 ];then
echo "$app_name server is restart failed!"
exit 1
fi
done
}

mod_pro
restart_app
