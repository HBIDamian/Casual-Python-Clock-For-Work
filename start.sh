#!/bin/bash

clear

# Define paths to your Python scripts
TIMER_SCRIPT="startTimer.py"
CLOCK_SCRIPT="startClock.py"

# Function to start the timer
start_timer() {
    echo "Starting Timer..."
    python3 "$TIMER_SCRIPT" > /dev/null 2>&1 &
}

# Function to start the clock
start_clock() {
    echo "Starting Clock..."
    python3 "$CLOCK_SCRIPT" > /dev/null 2>&1 &
}

# Function to start both timer and clock
start_both() {
    echo "Starting Timer and Clock..."
    start_timer
    start_clock
}

# Display the menu
echo "Please select an option:"
echo "1) Start Timer"
echo "2) Start Clock"
echo "3) Start Timer and Clock"
echo "4) Exit"
read -p "Enter your choice: " choice

# Handle the user's choice
case $choice in
    1)
        clear
        start_timer
        ;;
    2)
        clear
        start_clock
        ;;
    3)
        clear
        start_both
        ;;
    4)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid option. Please try again."
        ;;
esac

# Wait for user to exit the script by pressing any key
read -n 1 -s -r -p "Press any key to exit..."
 