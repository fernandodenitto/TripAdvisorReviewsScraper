# TripAdvisorScraper
Utility to get reviews from TripAdvisor Platform in but fashion

## What is it?

This small software written in Python allows you to obtain a dataset (in CSV format) made up of thousands of reviews obtained from the TripAdvisor platform in a massive way.

In particular:
You can get all the hotel links in a city listed on TripAdvisor
For each hotel obtained in the previous step, it is possible to obtain all the reviews in all the languages ​​present

## How it works

The executable files are written in Python 3 and there is no need to change the code to run them.

The "links_city_scraper.py" file requires you to enter the link relating to the city (on TripAdvisor) and produces as output a .txt file with the list of hotel links in the selected city.

The "scrape_advisor.py" file requests as input the name of the .txt file generated with the previous script and gets all the reviews of the hotels present in the .txt file. At the end of the script execution, a labeled dataset is generated in csv format with all the information present on TripAdvisor.

## How to Run the Scripts

You need to install Python3 on your computer and all the dependencies in the scripts:

> pip install bs4 

> pip install json 

> pip install pandas

> pip install request

If I missed something PLEASE read your console and install the other packages (and text me).


After that, simply go into the directory with the scripts and type:

> python3 links_city_scraper.py

> python3 scrape_advisor.py

## Disclaimer

The software produces a massive amount of data, also extrapolating the name and surname of visitors (if any).
For proper use these fields must be removed in order not to infringe privacy laws.

## Applications of this software

This software can be useful for various data studies including Sentiment Analysis and Text Mining. It is also possible to use quantitative data to be able to analyze trends in different cities on the platform.

## Please, cite me!

Please cite this repository if it is used for scientific purposes and if papers are produced using this software.

**Enjoy yourselves!**
