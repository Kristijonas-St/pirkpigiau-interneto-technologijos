#!/bin/bash

#TODO: ensure Flask stopping
cleanup() {
    echo "Stopping Flask and Streamlit..."
    pkill -f "flask run"
    pkill -f "streamlit run"
    exit 0
}

trap cleanup SIGINT

echo "Starting Flask..."
python3 login_func/back.py &

echo "Starting Streamlit..."
streamlit run main.py

wait


# stop Flask:
# lsof -i :5000
# kill -9 15654