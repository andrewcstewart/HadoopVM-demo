# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant::Config.run do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  config.vm.box = "centos6"
  config.ssh.username = "hadoop"
  
  config.vm.forward_port 80,5680
  config.vm.forward_port 22,5622
  config.vm.forward_port 50070,55670

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  config.vm.box_url = "http://download.frameos.org/vagrant/centos6-64-nochef-nopuppet.box"

  # Boot with a GUI so you can see the screen. (Default is headless)
  #config.vm.boot_mode = :gui


end
