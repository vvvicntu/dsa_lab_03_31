#!/bin/bash
python3 app.py &
sleep 2
python3 test_api.py
