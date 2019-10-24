<h1>Installation</h1>

<h2>Requirements</h2>
<ul>
	<li>Python3</li>
	<li>MongoDB</li>
</ul>

<h2>Flask</h2>

cd backend

python3 -m venv <path/to/environment>

~~~~~~~~~~~~~~~~~~~~~~~
If this doesn't work, try:

python3 -m venv --without-pip <path/to/environment>
source <path>/bin/activate
curl https://bootstrap.pypa.io/get-pip.py | python
deactivate
~~~~~~~~~~~~~~~~~~~~~~~

activate

pip install install.txt

<h2>React</h2>

yum install -y gcc-c++ make
curl -sL https://rpm.nodesource.com/setup_12.x | sudo -E bash -

npx create-react-app frontend

cd frontend
npm install

Go back to root folder

./start_server.sh

<h2>Setting routes and services</h2>

The file frontend/src/Actions.apiClient.js contains the basic route and port for the backend server. Change that accordingly to meet your needs.

The file backend/config.py contains all the backend routes (mongo url, secret, etc), which you will also have to change

Open the mongo shell by typing mongo
Build an index on the collection blacklist by typing db.blacklist.createIndex( { "createdAt": 1 }, { expireAfterSeconds: 86400 } )
Mongo deletes blacklisted tokens automatically after a week, in order to keep the collection small. However, for it to do so, it needs the collection to be indexed.