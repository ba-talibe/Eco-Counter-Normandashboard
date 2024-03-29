@echo off

call env\Scripts\activate

pip install -r requirements.txt

call env\Scripts\gunicorn main:server --workers 4