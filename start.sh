#virtualenv create

sudo apt-get -y install virtualenv
virtualenv ITT #project_name
cd ITT
source bin/activate
#install dependancies of environment
pip install flask
pip install flask-mysqldb
pip install pymysql
pip install flask-sqlalchemy
