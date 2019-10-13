# https://app.vagrantup.com/boxes/search

Vagrant.configure("2") do |config|
    # ubuntu 16.04 Xenial x64
    config.vm.box = "ubuntu/xenial64"
    config.vm.provider "virtualbox"


    # provisioning the ansible controller-slave (this VM is both a controller and a slave)
    config.vm.define "pan-peter" do |d|
      d.vm.hostname = "pan-peter"
      d.vm.network "private_network", ip: "192.168.50.10", virtualbox__intnet: true
      d.vm.provision :shell, path: "bootstrap.sh" # ansible installation
      d.vm.provision :shell, inline: "cd /vagrant/ansible/; ansible-playbook -i inventory.txt play.yml" # running the playbook
    end
	# provisioning a test VM (for remote rsyslog and NMAP testing)
	config.vm.define "peter-pan" do |d|
      d.vm.hostname = "peter-pan"
      d.vm.network "private_network", ip: "192.168.50.11", virtualbox__intnet: true
      d.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", "512"]
        vb.customize ["modifyvm", :id, "--cpus", "1"]
      end
    end
end
