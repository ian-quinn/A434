# Briefing

## Deployment on CentOS 7
All you need is to follow any deployment guide for static site. Here lists necessary commands specifically under environment: noc\tj-panyiqun virtual machine.
```
$ yum -y install epel-release
$ yum -y install supervisor nginx git
$ cd /home
$ git clone https://github.com/ian-quinn/a434.git
$ cp /home/a434/deployment/a434.conf /etc/nginx/conf.d/a434.conf
$ systemctl start nginx
# if failed go check parsing error first, like:
# nginx -t
$ systemctl enable nginx
# when configuration changed you may want to restart nginx but reload will do just fine
# systemctl restart nginx
# systemctl reload nginx
```
'403 Forbidden' is probably caused by SELinux. 2 ways to wind around it:
```
$ /usr/sbin/sestatus # check the status of SELinux
$ vi /etc/selinux/config
config $ SELINUX=disabled
# directly disable the SELinux then reboot your system. or allow access by:
$ chcon -R -t httpd_sys_content_t /home/a434/
```
You better keep the firewalld running.
