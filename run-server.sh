#!/bin/bash

check_success() {
    if [ $? -ne 0 ]; then
        echo "Error occurred: $1"
        exit 1
    fi
}

GANACHE_ACCOUNTS_FILE="./docker-config/ganache-data/ganache-accounts.json"

echo "Waiting for Ganache to start..."
while ! docker-compose logs ganache | grep -q "Listening on 0.0.0.0:8545"; do
    echo "Waiting for Ganache..."
    sleep 2
done
echo "Ganache has successfully started."
check_success "Failed to start Docker Compose."
sleep 2
cd ..

echo "Running Truffle migrations..."
if ! [ -x "$(command -v truffle)" ]; then
    echo "Truffle is not installed. Please install Truffle and try again."
    exit 1
fi

cd ./blockchain/
truffle migrate --reset
check_success "Truffle migration failed."
cd ../server

echo "Starting Python server..."
if [ ! -f server.py ]; then
    echo "server.py not found."
    exit 1
fi

python3 server.py
check_success "Failed to start server.py."

echo "All processes completed successfully."
