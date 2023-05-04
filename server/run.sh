#!/bin/bash

cd datacollector
python3 dataprovider.py &
python3 datacollector.py &
cd ..
python3 app.py