#!/bin/bash

cd ../stateServices
echo "Loading databases"
rm ./dbs/*
python3 sensorDAO.py
python3 loadsensors.py

echo "Databases Loaded"
