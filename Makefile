# Makefile for running the program and building required files

.DEFAULT_GOAL := run

# Run program
# Command: 'make' or 'make run' (while in the directory of the Makefile)
run: 1_Homepage.py
	streamlit run 1_Homepage.py