!#/bin/bash

echo "Welcome to Dis.co"

sleep 5

cp ../lesson_1/tests/test_1.py .

cp ../../requirements.txt .

brew install cmake
activate(){
    virtualenv boothenv

    source boothenv/bin/activate
}

pip3 install -r requirements.txt

python3 test_1.py

