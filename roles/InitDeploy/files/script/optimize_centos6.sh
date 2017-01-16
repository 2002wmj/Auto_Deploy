#!/bin/bash
#
#description: optimize centos6 gigold
#/usr/script/init_vmcopy.sh -- wangminjie added 2016-04-9

echo "这个是系统初始化脚本，请慎重运行！"

input_fun()
{
    OUTPUT_VAR=$1
    INPUT_VAR=""
    while [ -z $INPUT_VAR ];do
        read -p "$OUTPUT_VAR" INPUT_VAR
    done
    echo $INPUT_VAR
}
input_again()
{
MYHOSTNAME=$(input_fun "please input the hostname:")
#DOMAINNAME=$(input_fun "please input the domainname:")
DOMAINNAME=gigold-idc.com
CARD_TYPE=$(input_fun "please input card type(eth0):")
IPADDR=$(input_fun "please input ip address(192.168.100.1):")
NETMASK=$(input_fun "please input netmask(255.255.255.0):")
GATEWAY=$(input_fun "please input gateway(192.168.100.1):")
#MYDNS1=$(input_fun "please input DNS1(114.114.114.114):")
MYDNS1=172.16.1.10
MYDNS2=8.8.4.4
#MYDNS2=$(input_fun "please input DNS2(8.8.4.4):")
}
input_again
#获取网卡的MAC地址
sed -i "s/eth1/$CARD_TYPE/g" /etc/udev/rules.d/70-persistent-net.rules
MAC=$(cat /etc/udev/rules.d/70-persistent-net.rules |grep $CARD_TYPE|awk -F [=,]+ '{print $8}')
 
#SET COMPUTER NAME
cat >/etc/sysconfig/network <<ENDF
NETWORKING_IPV6=no
PEERNTP=no
NETWORKING=yes
HOSTNAME=$MYHOSTNAME
ENDF
 
cat >/etc/sysconfig/network-scripts/ifcfg-$CARD_TYPE <<ENDF
DEVICE=$CARD_TYPE
BOOTPROTO=static
HWADDR=$MAC
NM_CONTROLLED=yes
ONBOOT=yes
TYPE=Ethernet
IPADDR=$IPADDR
NETMASK=$NETMASK
GATEWAY=$GATEWAY
DNS1=$MYDNS1
DNS2=$MYDNS2
ENDF
 
#/etc/init.d/network restart
 
 
cat >/etc/hosts <<ENDF
127.0.0.1 $MYHOSTNAME $MYHOSTNAME.$DOMAINNAME localhost
::1 $MYHOSTNAME $MYHOSTNAME.$DOMAINNAME  localhost
$IPADDR $MYHOSTNAME $MYHOSTNAME.$DOMAINNAME  localhost
ENDF
 
cat >/etc/resolv.conf <<ENDF
nameserver $MYDNS1 
nameserver $MYDNS2 
ENDF
#domain $DOMAINNAME 
#search $DOMAINNAME


#关闭SEKINUX
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
setenforce 0
 
 
#修改文件打开数
echo "* soft nofile 65535" >> /etc/security/limits.conf  
echo "* hard nofile 65535" >> /etc/security/limits.conf
echo "* hard core 0" >> /etc/security/limits.conf

#优化用户进程打开数
sed -i 's/1024/20480/g' /etc/security/limits.d/90-nproc.conf
 
#优化内核参数
cat > /etc/sysctl.conf << ENDF
kernel.sysrq = 0
kernel.core_uses_pid = 1
kernel.msgmax = 1048576
kernel.msgmnb = 1048576
kernel.msgmni = 512
kernel.shmmax = 8255131648
kernel.shmall = 4294967296
kernel.shmmni = 80920
vm.swappiness = 6
vm.dirty_ratio = 20
vm.dirty_background_ratio = 10
net.ipv4.conf.lo.forwarding = 1
net.ipv4.conf.default.forwarding = 1
net.ipv4.conf.all.forwarding = 1
net.ipv4.ip_forward = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_synack_retries = 3
net.ipv4.tcp_syn_retries = 3
net.ipv4.conf.lo.arp_ignore = 1
net.ipv4.conf.lo.arp_announce = 2
net.ipv4.conf.all.arp_ignore = 1
net.ipv4.conf.all.arp_announce = 2
net.ipv4.tcp_wmem = 262144 1048576 8388608
net.ipv4.tcp_mem = 8388608 8388608 8388608
net.core.optmem_max = 40960
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.tcp_max_tw_buckets = 10000
net.ipv4.tcp_keepalive_time = 1200
net.ipv4.tcp_fin_timeout = 1
net.ipv4.tcp_timestamps = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 1
net.ipv4.ip_local_port_range = 2048 65000
net.ipv4.neigh.default.gc_thresh1 = 10240
net.ipv4.neigh.default.gc_thresh2 = 40960
net.ipv4.neigh.default.gc_thresh3 = 81920
net.core.rmem_default = 67108864
net.core.rmem_max = 134217728
net.core.wmem_default = 524288
vm.overcommit_memory = 1
net.core.wmem_max = 67108864
ENDF
sysctl -p 
 
#关闭系统不用的服务
for server in `chkconfig --list |grep 3:on|awk '{ print $1}'`
do
    chkconfig --level 3 $server off
done
 
for server in crond network rsyslog sshd
do
   chkconfig --level 3 $server on
done

#配置SSHD
#sed -i '/^#Port/s/#Port 22/Port 65535/g' /etc/ssh/sshd_config
sed -i '/^#UseDNS/s/#UseDNS yes/UseDNS no/g' /etc/ssh/sshd_config
#sed -i 's/#PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config
sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/g' /etc/ssh/sshd_config
#iptables -A INPUT -p tcp --dport 65535 -j ACCEPT
/etc/init.d/sshd restart


#设置密码长度和时间
sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   90/g' /etc/login.defs
sed -i 's/^PASS_MIN_LEN.*/PASS_MIN_LEN    8/g' /etc/login.defs


#设置终端超时时间
echo "TMOUT=3600">> /etc/profile

#设置时间时区同步
#yum -y install ntpdate
#/usr/sbin/ntpdate time.nist.gov
echo "#Ansible: Sync time in lan" >> /var/spool/cron/root
echo "*/5 * * * * /usr/sbin/ntpdate 172.16.1.10 1>/dev/null 2>&1" >> /var/spool/cron/root
reboot

#记录shell执行的每一条命令
cat >>/etc/profile << ENDF

export HISTTIMEFORMAT="[%Y-%m-%d %H:%M:%S] [\`who am i 2>/dev/null| \\
awk '{print \$NF}'|sed -e 's/[()]//g'\`] "
export PROMPT_COMMAND='\\
if [ -z "\$OLD_PWD" ];then
    export OLD_PWD=\$PWD;
fi;
if [ ! -z "\$LAST_CMD" ] && [ "\$(history 1)" != "\$LAST_CMD" ]; then
    logger -t \`whoami\`_shell_cmd "[\$OLD_PWD]\$(history 1)";
fi ;
export LAST_CMD="\$(history 1)";
export OLD_PWD=\$PWD;'
ENDF