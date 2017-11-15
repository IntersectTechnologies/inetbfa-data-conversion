# Data conversion and merge utilities for JSE equity data

Converts and merges data downloaded with the INETBFA Excel Add-In to csv format

[![Build Status](https://travis-ci.org/IntersectTechnologies/inetbfa-data-conversion.svg?branch=master)](https://travis-ci.org/IntersectTechnologies/inetbfa-data-conversion)

## Getting started:

The instructions below are for Windows:

Download and install [Anaconda](https://www.continuum.io/downloads) python distribution

If you do not already have git installed, download [git](https://git-scm.com/downloads) and follow the installation instructions.

Clone this repository in a shell/command prompt:

    git clone https://github.com/IntersectTechnologies/inetbfa-data-conversion.git

Install the required python packages with conda:

    conda install --yes --file requirements.txt

Install the doit task automation tool using pip:

    pip install doit

To initialise the directory structure run the bash script

    initialise.sh

**Download data**

To download new data you should have MS Excel installed and have the INETBFA Excel Add-Inn installed and configured.  This requires a subscription from http://www.inetbfa.com/ now IRESS (http://www.iress.co.za)

The data should be in a format compatible with the converter tools, stock tickers as the columns header and dates as the row index.  The converter tool only understands this specific format of the Excel files and expects the data frequency to be daily.  Each metric e.g. close, DY, PE etc should be saved in a separate file in the downloads folder

The Excel files are ignored in the master branch to avoid adding Excel file changes to the repository.

After the Excel files have been downloaded/refreshed you can now run the tasks to convert and calculated derived data by running the bash script:

    run.sh

you can also directly run:

    doit convert merge

The 'run.sh' bash script also copies the merged data to the master directory, so if you run the doit tasks directly you should copy the data yourself:

    cp -ruv ./merged/* ./master/

Several other commands also exist to calculate other metrics:

- adjusted_close (calculates the adjusted close by also including dividend distributions and adjusting the closing price backwards)
- book2market (calculates the Book-to-Market ratio)
- log_return (calculates the logartihmic returns from the adjusted close)
- monthly_avg_momentum (calculates the momentum from the average close price in a month)
- monthly_close_momentum (calculates the momentum from the month end close price)
- pead_monthly (calculate the momentum from the last earnings announcement date - Post Earnings Announcement Drift Momentum)
- resample_monthly (resamples the data to monthly data)
- data_per_ticker (Transforms the data to save all the metrics (columns) for one ticker in a file)

