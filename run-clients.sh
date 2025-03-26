#!/bin/bash

# Define the static path to the Python Tkinter app
app_path="./blockchain_client.py"

# Start 10 instances in parallel, each with a unique instance number
for i in $(seq 1 12); do
    # Run each instance in the background with the instance number as an argument
    python3 -m client.blockchain_client "$i" &
    echo "Started instance $i of the blockchain client  app."
    sleep .5
done

# Wait for all background processes to finish
wait
echo "All instances started."

