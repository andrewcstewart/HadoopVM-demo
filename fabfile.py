#!/usr/bin/env python

from fabric.api import run, put, cd, env, get, sudo, settings
from fabric.contrib.files import exists, append, contains
from fabric.decorators import hosts, task
from fabric.operations import local
import fabric
import pexpect
#from fexpect import expect
import os.path

tunnelsettings = {

        }

@task
def vagrant():
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    keyfile = result.split()[1]
    set_to('vagrant', '127.0.0.1', 5622, keyfile, uses_selinux=True)


def set_to(user, host, port=22, keyfile=None, uses_selinux=None):
    hostport = '%s:%d' % (host, port)
    tunnelsettings['touser'] = user
    tunnelsettings['tohost'] = host
    tunnelsettings['toport'] = port
    tunnelsettings['tohost_string'] = hostport
    tunnelsettings['tohosts'] = [hostport, ]
    tunnelsettings['tokey_filename'] = keyfile
    tunnelsettings['tohost_string'] = '%s@%s' % (user, host)
    tunnelsettings['tohost_uses_selinux'] = uses_selinux

def mysettings():
    return settings(
        user = tunnelsettings['touser'],
        password = None,
        key_filename = tunnelsettings['tokey_filename'],
        # disable_known_hosts = True
        hosts = [tunnelsettings['tohost'],],
        host_string = '%s@%s:%s' % (tunnelsettings['touser'],
                                    tunnelsettings['tohost'], 
                                    tunnelsettings['toport'])
        )    


#Installing Hadoop
#Configuring Hadoop
#Starting Hadoop
    
@task
def setup():
    with mysettings():
		#1.1 Installing Hadoop		
		if not exists("/usr/local/hadoop", use_sudo=False, verbose=False):
			run("wget http://download.nextag.com/apache/hadoop/common/hadoop-1.0.3/hadoop-1.0.3.tar.gz")
			sudo("mkdir /usr/local/hadoop")
#			sudo("chown hadoop:hadoop /usr/local/hadoop")
			sudo("chown vagrant:vagrant /usr/local/hadoop")
			with cd("/usr/local/hadoop/"):
				run("tar -xvzf /home/vagrant/hadoop-1.0.3.tar.gz")
		
		#1.2 Configuring Hadoop
		
		#Setup password-less ssh login
# [vagrant@127.0.0.1:5622] run: ssh-keygen -t rsa
# [vagrant@127.0.0.1:5622] out: Generating public/private rsa key pair.
# [vagrant@127.0.0.1:5622] out: Enter file in which to save the key (/home/vagrant/.ssh/id_rsa): 
# [vagrant@127.0.0.1:5622] out: /home/vagrant/.ssh/id_rsa already exists.
# [vagrant@127.0.0.1:5622] out: Overwrite (y/n)? y
# [vagrant@127.0.0.1:5622] out: Enter passphrase (empty for no passphrase): 
# [vagrant@127.0.0.1:5622] out: Enter same passphrase again: 
#		child = pexpect.spawn ('ftp ftp.openbsd.org')
#		child.expect ('Name .*: ')
#		child.sendline ('anonymous')
		if not exists("/home/vagrant/.ssh/id_rsa"):
			run("ssh-keygen -t rsa")
			run("cat .ssh/id_rsa.pub >> .ssh/authorized_keys")
			run("chmod 700 .ssh")
		
			#Create filesystem directories
			run("chmod 640 .ssh/authorized_keys")
		
		# note - determine way to do this test
		#ssh localhost
		#exit
		#ssh localhost
		#exit
		
		#Setup Pseudo Distributed configuration
#		run("mkdir /usr/local/hadoop/disk")
		with cd("/usr/local/hadoop/hadoop-1.0.3/"):
			if not exists("conf", use_sudo=False, verbose=False):
				run("mkdir -p conf.standalone conf.pseudo conf.cluster")
				run("mv conf conf.original")
				run("cp conf.original/* conf.standalone/")
				run("cp conf.original/* conf.pseudo/")
				run("cp conf.original/* conf.cluster/")
				run("ln -s conf.pseudo conf")
			
			#overwrite conf files
			run("cp /vagrant/conf/core-site.xml conf/core-site.xml")
			run("cp /vagrant/conf/hdfs-site.xml conf/hdfs-site.xml")
			run("cp /vagrant/conf/mapred-site.xml conf/mapred-site.xml")			

		#Set JAVA_HOME in hadoop-env Shell 
		sudo("yum -y install java-1.6.0-openjdk-devel.x86_64")
		#Is this ok [y/N]: Y

		run("echo 'export JAVA_HOME=/usr/lib/jvm/java' >> .bash_profile")  #TODO: apply this to config
		run("echo 'export PATH=/usr/local/hadoop/hadoop-1.0.3/bin:/usr/lib/jvm/java/bin:$PATH' >> .bash_profile")
		
		#Update /etc/hosts with current host info
		sudo("perl -p -i -e 's/%(line)s/%(line)s bdpuh/g' /etc/hosts" % {'line' : "127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4"})

		#Format NameNode
		with cd("/usr/local/hadoop/hadoop-1.0.3/bin"):
			run("./hadoop namenode -format")
		
@task
def start():
	# Start hadoop
	run("start-dfs.sh")
	run("start-mapred.sh")
	run("start-all.sh")
	
	# check
	run("jps")
