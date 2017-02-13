sudo git pull
sudo sed -i "s/8000/80/g" main.py
sudo npm run build-js
sudo python3 main.py
