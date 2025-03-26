# SHU-Electricity-Meter
SHU Uni Project

The Task

In this task you will build a simulation of a smart meter system for recording and managing domestic electricity
consumption.

You must build a client that acts as a smart meter. It should send readings to the server where they will be gathered,
verified, and stored. The server will calculate a bill based on the current electricity price which it will return to the
client. The client will display the bill. The client will send meter readings at random times but spaced no further than
60 seconds apart and no closer together than 15 seconds. You will demonstrate your system with at least twelve clients
connected concurrently to the server.

The client must run without any input from a user and must be able to:
-Authenticate onto the server with a secure connection
-Generate realistic randomly spaced readings.
-Send reading to the server.
-Display error messages if there is a communication problem between it and the server.
-Display a live bill that updates when each reading is transmitted.

The server must:
-Support multiple concurrent clients.
-Receive readings from each client.
-Store client details and readings.
-Calculate live bills and push them to clients.
-Log error messages if there is a communication problem between it and the server
-Push alerts to clients if there is a problem with the electricity grid.

Notes:
-You do not need to use a database. You may mock the database if you wish. When your system starts each
client should be associated with an existing set of readings.
-Your client can be a command line application a – it does not need to be a Web or desktop application.,
-Messages should be formatted using XML, JSON, or YAML.
-You must use a version control system such as Github. You will be asked to give a link to your shared Github
repository and we will expect to see commits made by all members of the team



TO RUN THE CODE PLEASE FOLLOW THE STEPS BELOW: 

- Run the run-docker.sh shell script to start the ganache instance. NOTE: You must have docker installed.
- Run the run-server.sh shell script to deploy the smart contract to the ganache blockchain instance. This will also start the grid alert emitter script.
- In a new terminal instance run the run-clients.sh shell script to start 12 instances of the smart meter.