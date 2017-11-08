#virtualenv create

sudo apt-get -y install virtualenv
virtualenv ITT #replace_with_your_project_name
cd ITT
source bin/activate
#install dependancies of environment
pip install flask
pip install flask-mysqldb
pip install pymysql
pip install flask-sqlalchemy
