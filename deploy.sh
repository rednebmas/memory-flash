if ! [ -x "$(command -v ruby)" ]; then
	sudo apt-get install ruby-dev
fi
if ! [ -x "$(command -v sass)" ]; then
	sudo gem install sass --no-user-install
fi

sudo git checkout -- .
sudo git pull
sudo sed -i "s/8000/80/g" main.py
sudo npm update
sudo npm run compile
sudo python3 main.py
