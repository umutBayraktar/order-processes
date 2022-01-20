virtualenv -p python3.8 unittestenv
source unittestenv/bin/activate
pip3 install -r requirements.txt
cd orderlist
python manage.py test