#!/bin/bash
echo "Running web.sh ..."
source venv/bin/activate
flask run --host=0.0.0.0 --port=80