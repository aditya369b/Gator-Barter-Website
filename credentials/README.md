# Credentials Folder

## The purpose of this folder is to store all credentials needed to log into your server and databases. This is important for many reasons. But the two most important reasons is
    1. Grading , servers and databases will be logged into to check code and functionality of application. Not changes will be unless directed and coordinated with the team.
    2. Help. If a class TA or class CTO needs to help a team with an issue, this folder will help facilitate this giving the TA or CTO all needed info AND instructions for logging into your team's server. 


# Blow is a list of items required. Missing items will causes points to be deducted from multiple milestone submissions.

1. Server URL or IP
2. SSH username
3. SSH password or key.
    <br> If a ssh key is used please upload the key to the credentials folder.
4. Database URL or IP and port used.
    <br><strong> NOTE THIS DOES NOT MEAN YOUR DATABASE NEEDS A PUBLIC FACING PORT.</strong> But knowing the IP and port number will help with SSH tunneling into the database. The default port is more than sufficient for this class.
5. Database username
6. Database password
7. Database name (basically the name that contains all your tables)
8. Instructions on how to use the above information.

# Most important things to Remember
## These values need to kept update to date throughout the semester. <br>
## <strong>Failure to do so will result it points be deducted from milestone submissions.</strong><br>
## You may store the most of the above in this README.md file. DO NOT Store the SSH key or any keys in this README.md file.


## Configuration Information
1. Server URL - http://ec2-18-189-193-11.us-east-2.compute.amazonaws.com or IP - http://18.189.193.11
2. SSH username
3. SSH key - Uploaded to the credentials folder.
4. Instructions on how to use the above information are as follows:

How to ssh as root user
- Aquire the appropriate .pem file
- Make sure the permissions for said pem file are either 600 or 400
- ssh in using the pem file as an identity and "ubuntu" as the user like this
- ssh -i [NAME_OF_PEM_FILE].pem ubuntu@[CURRENT_IP_ADDRESS]
- If you haven't already sshed in, type yes to add the ip address to your known ones

Please Note:
<BR>Our App should be running through a service on top of nginx
the service is "app.service" and the nginx service is simply "nginx.service"
If for whatever reason you make a change to the app as root on the server you will need to restart both services to see your change
you might be able to get away with just restarting the app service, but it is safer to restart both.

PLEASE DON'T CHANGE ANY SERVER CONFIGURATIONS WITHOUT CONTACTING THE SERVER ADMIN FIRST
