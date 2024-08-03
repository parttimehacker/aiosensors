#/usr/bin/bash
sudo cp $1.py /usr/local/$1
sudo cp ./logging.ini /usr/local/$1
sudo cp -r ./pkg_classes /usr/local/$1
sudo cp $1.service /lib/systemd/system/$1.service
sudo systemctl daemon-reload
sudo systemctl enable $1.service
sudo systemctl restart $1
echo "Updated systemctl for $1"

