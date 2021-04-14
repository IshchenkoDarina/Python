sudo apt update
sudo apt install -y python3-pip python3-dev libpq-dev nginx git
pip install --upgrade pip
pip install virtualenv
sudo mkdir -p /var/www/unix-project
sudo chown 1000:1000 /var/www/unix-project
cd /var/www/unix-project
git clone https://github.com/IshchenkoDarina/Python.git .
virtualenv unix-project
source unix-project/bin/activate
pip install django-bootstrap4 django_registration django gunicorn 
/var/www/unix-project/manage.py migrate
#sudo ufw allow 8000
deactivate

echo "reset systemctl"
#sudo systemctl daemon-reload
sudo systemctl stop gunicorn
sudo rm -f /etc/systemd/system/gunicorn.service

echo "setup gunicorn.service"
sudo touch /etc/systemd/system/gunicorn.service
sudo chown 1000:1000 /etc/systemd/system/gunicorn.service
sudo cat << EOL > /etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/unix-project
ExecStart=/var/www/unix-project/unix-project/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/unix-project/unix-project.sock news.wsgi:application

[Install]
WantedBy=multi-user.target
EOL

sudo chown root:root /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
echo "start gunicorn"
sudo systemctl start gunicorn
echo "enable gunicorn"
sudo systemctl enable gunicorn

echo "setup nginx"
sudo rm -f /etc/nginx/sites-enabled/default
sudo rm -f /etc/nginx/sites-available/unix-project
sudo touch /etc/nginx/sites-available/unix-project
sudo chown 1000:1000 /etc/nginx/sites-available/unix-project
sudo cat << EOL > /etc/nginx/sites-available/unix-project
server {
listen 80;
server_name localhost;

location = /favicon.ico { access_log off; log_not_found off; }

location / {
include proxy_params;
proxy_pass http://unix:/var/www/unix-project/unix-project.sock;
}
}
EOL

sudo ln -s /etc/nginx/sites-available/unix-project /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
