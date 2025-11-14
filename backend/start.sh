#!/bin/bash
# Start script for Render
# Render will use this if specified, otherwise uses startCommand from render.yaml

uvicorn main:app --host 0.0.0.0 --port $PORT

