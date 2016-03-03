# Data conversion and management utilities

Converts and merges data downloaded with the INETBFA Excel Add-In to csv formats

## Getting started:

Install python on your system if it is not already installed:

- Python 2.7+ shaould work
- Tested on Python 3.4+
- Recommended Python 3.5 as part of the Anaconda python distribution:  https://www.continuum.io/downloads

Install python doit automation tool:

    pip install doit

Clone this repository

    git clone https://github.com/IntersectTechnologies/inetbfa-data-conversion.git
    

**Refresh data**

Update the data in the downloads folder by refreshing each of the Excel Workbooks (assuming you have the INETBFA Excel  Add-Inn installed and configured properly)

**Convert data**

Run the script run.sh in a shell

    ./run.sh
