virtualenv -p python3.8 unittestenv
source unittestenv/bin/activate
pip3 install -r requirements.txt
python manage.py test