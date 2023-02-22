# WWWatcher


WWWatcher is a Python application that watches a directory for Excel files and processes any Excel files found. 
Specifically, it looks for tables containing information about consumables, compact panels, and panels, and posts this 
information to an Orion Broker using Fiware.

## Installation

1. Clone this repository:

```bash
git clone https://github.com/iaggocapitanio1/WWWatcher
```

2. Change to the directory:

```bash
cd WWatcher
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Usage 

1. Ensure that you have an Orion Broker set up and that you have its URL and headers in the settings.py file.
2. Modify the settings.py file to set the correct path to the directory you want to watch for Excel files.
3. Run the main.py file:

### Acknowledgments

This project was inspired by the watchdog library and the Fiware platform.