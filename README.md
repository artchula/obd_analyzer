OBD记录器

1.装系统
1.1. 无屏幕和键盘配置树莓派WiFi和SSH
1.1.1. 在 boot 分区，也就是树莓派的 /boot 目录下新建 wpa_supplicant.conf 文件，按照下面的参考格式填入内容并保存 wpa_supplicant.conf 文件
--------------------------------------------------------------------------------
country=CN
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
 
network={
ssid="WiFi-A"
psk="12345678"
key_mgmt=WPA-PSK
priority=1
}
 
network={
ssid="WiFi-B"
psk="12345678"
key_mgmt=NONE
priority=2
scan_ssid=1
}
--------------------------------------------------------------------------------
1.1.2. 说明以及不同安全性的 WiFi 配置示例：
#ssid: 		网络的ssid
#psk: 		密码
#key_mgmt: 	WEP加密或无密码填写 “ NONE ” ， WPA/WPA2加密填写 “ WPA-PSK ”
#priority:		连接优先级，数字越大优先级越高（不可以是负数）
#scan_ssid:	连接隐藏WiFi时需要指定该值为1

1.2. 开启 SSH
同样在 boot 分区新建一个文件，空白的即可，文件命名为 ssh，注意要小写且不要有任何扩展名

1.3. 树莓派系统：raspbian
默认的用户名：pi
默认密码：raspberry

1.4. 修改时区
1.4.1. 配置
sudo raspi-config 进入配置界面
Localisation Options 》Change Timezone 》Asia 》Shanghai 》Finish
1.4.2. 测试
输入 date，查看当前时间是否正确

2. 基础配置
2.1. 修改密码
sudo passwd pi		#修改 Pi 密码 
sudo passwd root 		#设置 root 密码 
su root 				#切换到 root 用户 
su pi				#切换到 pi 用户

2.2. 更换镜像源
sudo nano /etc/apt/sources.list
添加阿里云镜像，将默认地址 mirrordirector.raspbian.org 替换为 mirrors.aliyun.com/raspbian/

2.3. 更新系统和软件
sudo apt update
sudo apt upgrade
sudo apt dist-upgrade

2.4. 安装vim
sudo apt install vim

2.5. 修改主机名
2.5.1. 修改 hosts 文件
sudo vim /etc/hosts
你会看到下面这行：" 127.0.1.1    raspberrypi "，将 raspberrypi 替换成要修改的名字
2.5.2. 修改 hostname 文件
sudo vim /etc/hostname
默认情况下，这个文件只包含 raspberrypi 这一个名字。请将这里也替换成要修改的名字
2.5.3. 重启树莓派
直接断电

3. 安装软件
3.1. 安装git
3.1.1. 安装
sudo apt install git
3.1.2. 配置
用户名（必选）：	git config --global user.name "runoob"
邮箱（必选）：	git config --global user.email test@runoob.com
文本编辑器：		git config --global core.editor vim
差异分析工具： 	git config --global merge.tool vimdiff
缓存大小：		git config --global http.postBuffer 524288000
3.1.3. 查看配置
git config --list

3.2. 安装pip3
sudo apt-get install python3-pip

3.3. 安装python-can
3.3.1. Using this routine requires first installing the library:
sudo pip3 install python-can
3.3.2. Then make sure your mcp2515 kernel driver is open:
sudo vim /boot/config.txt
3.3.3. And add the following:
# Enable can (loads mcp2515)
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25,spimaxfrequency=1000000
3.3.4. Then restart the raspberry pi：
sudo reboot
3.3.5. Test
send run:
sudo python send.py
Receiving run:
sudo python receive.py
You will see the following:
Timestamp: 1527240783.548918        ID: 0123    S          DLC: 8    00 01 02 03 04 05 06 07

3.4. 从远程仓库github下载代码
 sudo git clone https://github.com/zrs703/obd_analyzer.git

3.5. 安装samba服务
3.5.1. 安装
sudo apt-get install samba samba-common-bin
3.5.2. 配置
sudo vim /etc/samba/smb.conf
在文件最下面加上以下内容，这里设置/home/pi/Public为共享文件夹
[can_msg]
   comment = Public Storage  					# 共享文件夹说明
   path = /home/pi/obd_analyzer/data/can_msg 	# 共享文件夹目录
   read only = no 							# 不只读
   create mask = 0777 						# 创建文件的权限
   directory mask = 0777 					# 创建文件夹的权限
   guest ok = yes 							# guest访问，无需密码
   browseable = yes 						# 可见
重启Samba服务
sudo samba restart
3.5.3. 设置文件夹权限
创建共享文件夹
sudo mkdir -p /home/pi/obd_analyzer/data/can_msg
在Samba配置文件设置过权限后，还需要在系统中将共享文件夹的权限设置为同配置文件中相同的权限，这样才能确保其他用户正常访问及修改文件夹内容
sudo chmod -R 777 /home/pi/obd_analyzer/data/can_msg
或者直接创建文件夹时修改权限
sudo mkdir -pm 777 /home/pi/obd_analyzer/data/can_msg
3.5.4. 测试
配置完成后即可从局域网内其他电脑访问共享文件夹，Windows下访问目录为 \\IP\Folder 或\\hostname\Folder，例如：
\\10.10.2.134\can_msg 
或
\\obd_analyzer_1\can_msg

3.6. 开机启动
3.6.1. 配置
sudo vim /etc/rc.local
在 exit 0 前面加入一行，如下：
su pi -c "sudo python3  /home/pi/obd_analyzer/src/obd_analyzer.py  &"
3.6.1.1. su pi :是以pi用户执行，  -c：执行完回到当前的用户
3.6.1.2. 调用文件内必须采用绝对地址
3.6.2. 测试
cd 				# 进入用户根目录
sudo /etc/rc.local 	# 没报错表示通过测试
