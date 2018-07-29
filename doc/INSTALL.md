## How to install
In this guide, I will show you how to install battery using apache and mod_wsgi.
At first, You need to install apache and mod_wsgi to use battery.
```
$ sudo yum install -y httpd mod_wsgi
```
and next clone battery repository. I assume that the application root directory is your home directory.
```
$ cd ~
$ git clone https://github.com/d2verb/battery
```
You alse need to change the group of battery directory and files under it so that apache can read or write them.
```
$ sudo chgrp -R apache ~/battery
```
Next, you need to write a script for mod_wsgi. I will show you an example.
```
$ cd ~/battery
$ cat battery.wsgi
import sys, os
sys.path.insert(0, "<your_home_dir>/battery")

os.environ["FLASK_ENV"] = "production"

from battery import create_app
application = create_app()
$ sudo chgrp apache batter.wsgi
$ chown g+r battery.wsgi
$ chown g+x battery.wsgi
```
And last, you need to modify the httpd.conf and start httpd.
```
$ cat /etc/httpd/conf/httpd.conf
.
.
.
# For wsgi
LoadModule wsgi_module modules/mod_wsgi.so
WSGISocketPrefix /var/run/wsgi

<VirtualHost *:80>
  WSGIDaemonProcess battery user=<your_username> group=apache threads=4
  WSGIScriptAlias / <your_home_dir>/battery/battery.wsgi
  WSGIScriptReloading On

  <Directory <your_home_dir>/battery>
    WSGIProcessGroup battery
    WSGIApplicationGroup %{GLOBAL}
    Require all granted
  </Directory>
</VirtualHost>
$ sudo systemctl start httpd
```
