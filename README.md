A simple Django-based CMS built for the [OpenDev](http://www.opendevconf.com/) Conference.


# General environment setup
```bash
sudo apt install python-dev python-pip libjpeg-dev libssl-dev
sudo pip install virtualenv
```

# Project setup

```bash
git clone https://github.com/OpenStackweb/opendev.git opendev

cd opendev
virtualenv -p python3 .env
source .env/bin/activate

# Install reqs
pip install -r requirements.txt 

# Copy the settings template.
cp opendev/settings_local.py.template opendev/settings_local.py

# Make sure to review and edit the new settings file.
# You may want to edit ALLOWED_HOSTS to include local IP,
# setup a proper database backend, contact info, etc.
cat opendev/settings_local.py

# Setup initial DB
python manage.py migrate
```


# Development

```bash
# Running the dev server
# Defaults to 127.0.0.1
# Use 0.0.0.0:8000 to bind to the external IP
python manage.py runserver 0.0.0.0:8000
```