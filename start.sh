#!/bin/bash

clear

# Define paths to your Python scripts
TIMER_SCRIPT="startStopwatch.py"
CLOCK_SCRIPT="startClock.py"

# Function to start the Stopwatch
start_stopwatch() {
    echo "Starting Stopwatch..."
    python3 "$TIMER_SCRIPT" > /dev/null 2>&1 &
}

# Function to start the clock
start_clock() {
    echo "Starting Clock..."
    python3 "$CLOCK_SCRIPT" > /dev/null 2>&1 &
}

# Function to start both Stopwatch and clock
start_both() {
    echo "Starting Stopwatch and Clock..."
    start_stopwatch
    start_clock
}

# Display the menu
echo "Please select an option:"
echo "1) Start Stopwatch"
echo "2) Start Clock"
echo "3) Start Stopwatch and Clock"
echo "4) Exit"
read -p "Enter your choice: " choice

# Handle the user's choice
case $choice in
    1)
        clear
        start_stopwatch
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
 