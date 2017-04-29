# Data conversion and merge utilities for JSE equity data

Converts and merges data downloaded with the INETBFA Excel Add-In to csv formats

[![Build Status](https://travis-ci.org/IntersectTechnologies/inetbfa-data-conversion.svg?branch=master)](https://travis-ci.org/IntersectTechnologies/inetbfa-data-conversion)

## Getting started:

If you do not already have git installed, download [git](https://git-scm.com/downloads) and follow the installation instructions.

Clone this repository in by typing the following into a command line:

    git clone https://github.com/IntersectTechnologies/inetbfa-data-conversion.git

To build and run the data conversion tool we use vagrant to set up a complete environment.

Download and install [Vagrant](https://www.vagrantup.com/downloads.html)

The Vagrant file in the repository has the complete configuration for the environment and will download and install all the dependencies when typing:

    vagrant up

on the command line.

This will start a virtual machine with the newest Miniconda Python 3 distribution from Continuum Analytics installed.  All the package dependencies will be installed as part of the provisioning of the vagrant virtual environment.

After the virtual machine is running, type the following:

    vagrant ssh


**Download data**

To download new data you should have MS Excel installed and have the INETBFA Excel Add-Inn installed and configured.  This requires a subscription from http://www.inetbfa.com/
Update the data in the downloads folder by opening each of the Excel Workbooks, going to the INETBFA tab and refreshing the imported data.

The Excel files are ignored in the master branch to avoid adding Excel file changes to the repository, but you can get a copy by checking out the initialise branch:

    git checkout initialise

Go back to the master branch:

    git checkout master

and run the following command:

    doit convert merge adjust_close book2market

This will create the following files:



After the conversion has completed you can again destroy the virtualised environment with:

    vagrant destroy
