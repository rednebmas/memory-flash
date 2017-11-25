if ! [ -x "$(command -v ruby)" ]; then
	sudo apt-get install ruby-dev
fi
if ! [ -x "$(command -v sass)" ]; then
	sudo gem install sass --no-user-install
fi

sudo git checkout -- .
sudo git pull
pip3 install -r requirements.txt
sudo npm update
sudo npm run compile
sudo python3 main.py release
