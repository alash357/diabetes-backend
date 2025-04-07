#!/bin/bash

# Make sure to give this file execution permissions:
# chmod +x start.sh

uvicorn app.main:app --host 0.0.0.0 --port 10000
