
## PyTracker

A simple python application to track the time and usage of application in your system Mac or PC. 

## Getting Started

To use this project it’s pretty much straight forward with the only requisite being a working python library preferable python3 on your system. 

### Installing and Usage

- Clone the project to your location of choice.
- Navigate into the project to the location of `pytimer.py` and run the file using python.

    ```
    python pytimer.py
    ```

- The program will start executing with the terminal showing what application has been used previously with timer having started for the application you are currently on.
- All the data about the applications being tracked will be saved in JSON format in `activities.json`.
- In case of websites visited in Chrome or Safari, the individual websites are tracked as independent application.
- Also when using an application for which an entry had already been added to `activities.json`, it will be coupled together under the same program entry.

### Languages used

- Python
