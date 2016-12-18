#### ** WARNING DO NOT RUN ON PERSONAL COMPUTER, CAN CAUSE EXTREME HARM **
# CPSC-456 Network Security Fundamentals
## Assignment 1
### Fall 2016
#### Due Date:  10/21/2016 at 11:59 pm 

#### <b>Overview:</b>
 In class we learned about computer worms; self-replicating malware programs which break into
vulnerable systems and use the systems they compromise to launch attacks against other vulner-
able systems.  Different worms spread using different tactics.  Some spread through email, some
through the web, while others take advantage of file sharing networks as well as other means.
In this assignment you are going to author a worm which uses the Secure Shell (SSH) service to
spread, download malicious payload, and, finally, steal data from compromised systems.
You are going to implement three distinct types of worms described below.  All of the worms
that follow make use of SSH and Python skills you acquired during our in-class exercise.

   1. <b> Worm 1: The Replicator: </b> A basic worm which scans its local network to detect systems running SSH service, attempts to break into one of those systems using a dictionary attack (i.e.  password guessing attack), copies itself onto the compromised system, executes itself on the compromised system, and repeats the same process from the compromised system. This particular worm carries no malicious payload.
   2. <b>Worm 2: The Extorter:</b> This worm is similar to the replicator worm, but in addition to spreading it also downloads an encryption program and uses it to encrypt user's files in the Documents directory and leaves an extortion message on the user's desktop.
   3. <b>Worm 3: The Password File Thief:</b> This worm is similar to the replicator,  except from every infected system it copies the /etc/passwd file to the attacker's server (that is, the VM from which the attack was originally initiated).

#### <b>Requirements:</b>
This section lays out the specific requirements for each of the three types of worms.  The repli-
cator,  extorter,  and  password  file  thief  worms  shall  be  implemented  in separate files  named replicator_worm.py, extorter_worm.py, and passwordthief_worm.py, respectively.  The detailed requirements for each type of worm are as follows:

<b>The Replicator Worm:</b>

  1. This worm shall be executed using command line python replicator worm.py ARG1 ARG2 ...ARGN from the origin system (the use of arguments is optional).
  2. When  executed,  the  worm  shall  scan  its  local  area  network  for  presence  of  other systems running SSH service.
  3. The worm shall carry a dictionary of possible user names and passwords.  This list shall include both correct and incorrect passwords for all VMs on the node.
  4. The worm shall attempt to login into discovered host systems using SSH user names and passwords in its dictionary until it successfully logs into one of the hosts or until  it  has  tried  all  user  names  and  passwords  against  all  hosts  without  success. If  the  worm  is  unable  to  guess  the  credentials  for  any  of  the  discovered  systems, it  terminates.   Otherwise,  the  worm  checks  if  the  remote  system  has  already  been infected.  If so, then it skips this system and moves on to attacking other systems. If not so, the worm copies itself onto the compromised system, executes itself on the newly compromised system, and terminates on the current system.
  5. Once executed on the remote system, the worm shall check if the system is is already infected  and  if  so,  terminates.   Otherwise,  the  worm  attempts  to  spread  to  other systems using the above-stated process.  This check prevents two copies of the same worm from executing on the same system at the same time.
  6. When attempting to guess system credentials, the worm shall only use the user names and passwords in its dictionary.
  7.The worm shall not launch attacks from the same system more than once.

 <b>The Extorter Worm:</b>

  1. This worm shall be executed using command line python extorter worm.py ARG1 ARG2 ...ARGN from the origin system (the use of arguments is optional).
  2. This worm shall encompass all features and conform to all requirements of the replicator worm, except the above requirement.
  3. This worm shall download the encryption program from the http://ecs.fullerton.edu/~mgofman/openssl URL.
  4. After downloading the openssl program the worm shall create a tar archive  of the /home/cpsc/Documents directory and encrypt it using the openssl program. After the Documents directory  has  been  encrypted,  the  worm  shall  delete  the /home/cpsc/Documents directory and leave a note telling the user that his files have been encrypted and that he/she needs to purchase the decryption key from the attacker in order to get the files back.
  5. All files shall be encrypted using password cs456worm (which openssl program accepts as one of the arguments; please see the next section for details).
  6. This worm shall leave the files on the attacker's system unharmed.
  
<b>The Password File Thief Worm:</b>

  1. This worm shall be executed using command line python passwordthief worm.py ARG1 ARG2 ...ARGN from the origin system (the use of arguments is optional).
  2. This worm shall encompass all features and conform to all requirements of the replicator worm, except the requirement above.
  3. When the is executed on a victim system, it shall copy the /etc/passwd file,  the file  containing  information  about  system  user  names  and  passwords,  back  to  the attacker's system (that is, the system from which the attack was originally initiated).
  4. When the /etc/passwd file is copied to the attacker's system it shall be named as passwd < IP of the victim system>. For example, passwd 192.168.1.101.
  5. This worm shall not touch the password FIle on the attacker's system (that is, the system from which the attack was originally initiated).

#### <b>Technical Guidelines:</b>

  1. This assignment MUST be completed using Python
  2. Your assignment MUST run on ThoTh lab systems (or VM)
  3. Write a README file (text file, do not submit a .doc file) which contains
    - Names and email addresses of all team members.
    - Your node number, password (if you changed it), and the name of the VM containing a copy of the worm from which the initial attack can be launched.
    - How to execute your program.
    - Whether you implemented the extra credit.
    - Anything special about your submission that we should take note of
