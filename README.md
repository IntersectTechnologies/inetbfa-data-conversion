# Data conversion and merge utilities for JSE equity data

Converts and merges data downloaded with the INETBFA Excel Add-In to csv formats

[![Build Status](https://travis-ci.org/IntersectTechnologies/inetbfa-data-conversion.svg?branch=master)](https://travis-ci.org/IntersectTechnologies/inetbfa-data-conversion)

## Getting started:

Install python on your system if it is not already installed:

- Python 2.7+ should work
- Tested on Python 2.7+, 3.4+
- Get the Anaconda python distributio from:  https://www.continuum.io/downloads

Install python doit automation tool:

    pip install doit

Clone this repository in an empty directory

    git clone https://github.com/IntersectTechnologies/inetbfa-data-conversion.git

**Download data**

To download new data you should have MS Excel installed and have the INETBFA Excel Add-Inn installed and configured.  This requires a subscription from http://www.inetbfa.com/
Update the data in the downloads folder by opening each of the Excel Workbooks, going to the INETBFA tab and refreshing the imported data.

The Excel files are ignored in the master branch to avoid adding changes to the repository, but you can get a copy by checking out the initialise branch:

    git checkout initialise

**Convert data**

To convert the data run the doit task from the command line:

    doit convert

**Merge the data**

To merge the newly converted data with the exisiting data

    doit merge    

**Adjustment tasks**

After the data has been updated the adjustment tasks can be run.

    doit adjust_close book2market

**Transformation tasks**

If you have a complete dataset in the correct format you can run the available transformation tasks.  Currently none is available, but momentum and moving_avg and resampling is planned for the near future... watch this space!
