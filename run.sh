#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python 3 is not installed. Please install Python 3 and try again.${NC}"
        exit 1
    fi
}

# Function to check if virtual environment exists
check_venv() {
    if [ ! -d "venv" ]; then
        echo -e "${BLUE}Creating virtual environment...${NC}"
        python3 -m venv venv
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to create virtual environment. Please install python3-venv and try again.${NC}"
            exit 1
        fi
    fi
}

# Function to activate virtual environment
activate_venv() {
    source venv/bin/activate
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to activate virtual environment.${NC}"
        exit 1
    fi
}

# Main script
echo -e "${BLUE}Starting Valorant Overlay System${NC}"

# Check Python installation
check_python

# Setup virtual environment
check_venv
activate_venv

# Check if this is first run
if [ ! -f "venv/INSTALLED" ]; then
    echo -e "${BLUE}First run detected. Running setup...${NC}"
    python3 setup.py
    touch venv/INSTALLED
fi

# Run the updater
echo -e "${GREEN}Starting overlay updater...${NC}"
python3 app/updater.py

# Deactivate virtual environment
deactivate
