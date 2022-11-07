# AV Signage Setup

- AWS Ubuntu Image
- AWS network/firewall rules - allow ssh and http from local network
- Install Apache2 (sudo apt install apache2)
- Apache Config setup for CGI (/etc/apache2/)
	- Create alias for mods-available/cgi.load in mods-enabled/
	- Edit sites-available/---/default.conf
		- DocumentRoot /var/www/html
		```
			<Directory "/var/www/html">
	            		allow from all
       		    		Options None
    	    			Require all granted
        	  	</Directory>
			
	  	 ScriptAlias /cgi-bin/ "/var/www/cgi-bin/"
			<Directory "/var/www/cgi-bin">
    	    		Options +ExecCGI 
	    		AddHandler cgi-script .cgi .py
       			</Directory>
- Install python venv and pip
	-  sudo apt install python3.10-venv
	-  sudo apt-get install python3-pip
- Setup environment variable 'BOX_AV_SIGNAGE' (sudo nano /etc/environment)
- Setup venv in /var/www/venv (python3 -m venv venv)
	- pip3 install pandas
	- pip3 install openpyxl

- Copy cgi-bin folder to /var/www/
- Copy /html/signage/ folder to /vaw/www/html/
