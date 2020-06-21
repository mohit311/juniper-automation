This script will zip the var logs onto RE0 and RE1 of Juniper routers and get the RSI and var logs files and sftp over to SFTP server. After that it will transfer them over to windows folder using pysftp module. This can surely be tweaked as per requirement.

As there are no Pyez native commands to directly get files from Backup RE hence we have used StartShell functionality to get around it.
