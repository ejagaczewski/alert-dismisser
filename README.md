##alert-dismisser

Migration helper. Pulls a list of dismissed alerts from one Prisma Cloud tenant with policy name and resource ID and compares them to another. Common policy and resource pairs are identified along with alert IDs which are then sent for dismissal.

##Usage

Modify dismiss-puller.py and alert-dismisser.py to include access keys and correct the API URLs.

Run dismiss-puller.py before migrating accounts to a new tenant to generate a list of dismissed alerts.

Run alert-dismisser.py after migrating accounts to a new tenant to dismiss alerts which were dismissed previously on the old tenant.

#Warning : This is a proof of concept. Test prior to running in production. 

##Requirements and Dependencies

Python 3.X

Requires Pandas

sudo pip install pandas

Requires Requests

sudo pip install requests
