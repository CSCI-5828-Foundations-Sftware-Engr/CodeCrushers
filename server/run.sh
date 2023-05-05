#!/bin/bash

cd datacollector
python3 dataprovider.py &
python3 datacollector.py &
cd ..
cd dataanalyzer
python3 dataanalyzer.py &
cd ..
python3 app.py