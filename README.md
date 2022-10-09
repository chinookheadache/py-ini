# py-ini
zac fawcett
Python Script that outputs machine data based on contents of an INI file

The config (ini) file is read when the script is run. The config file can be customized to change the output of the script.

File Names:
- projectini
- projectoutput
- py-ini


Running script:
1. Start script
2. Script reads a configuration file projectini that contains the following:
        a. Name of output file (projectoutput)
        
        b. Filter options pertaining to logs
        
        c. Constants pertaining to actions of the script
        
3. Menu appears with instructions:


Selection---

1 System accounts

2 System logs

3 Generate Report

Press Enter to exit


1. prints to screen all accounts and their group associations sorted alphabetically by account name

2. prints to screen system logs from /var/log/  based on the criteria specified in the projectini file

3. Overwrites the previous file (file path/name specified in projectini file)
    	#Name of computer
        
    	#Date and time (formatted)
        
   	#Results from option 1
        
    	#Results from option 2
