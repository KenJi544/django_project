#/bin/bash

pip install requirements
source bin/activate
python src/hwdjango/manage.py runserver
