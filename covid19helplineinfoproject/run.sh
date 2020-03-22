sudo pkill python3*
sudo python3 manage.py migrate
sudo nohup python3 manage.py runserver 0.0.0.0:80 &
