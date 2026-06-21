\# Air Raid Alert Time Series Forecast (Ukraine)



A small, self-contained Python project that forecasts the number of oblasts (regions) under air raid alert per day in Ukraine, using a classical time series forecasting technique (Holt-Winters Exponential Smoothing).



\---



\## What this project does



1\. Loads a bundled CSV of real, historical air raid alert events.

2\. Aggregates those events into a daily time series: one number per day, representing how many of Ukraine's 25 oblasts had at least one active alert that day.

3\. Fits a forecasting model on that series and evaluates how accurate it would have been on the most recent two weeks.

4\. Forecasts the next 14 days.

5\. Saves a chart (PNG) and the forecast numbers (CSV) to the outputs/ folder.



\## The data



\* Source: Publicly available, actively-maintained dataset that aggregates official Ukrainian air raid alert announcements.

\* Refreshing the data: Run py -m scripts.fetch\_live\_data to overwrite and get the latest updates.



\## Project structure



\* data/raw/alerts\_sample.csv <- bundled real data

\* outputs/forecast\_chart.png <- generated chart

\* outputs/forecast\_values.csv <- generated forecast numbers

\* scripts/fetch\_live\_data.py <- refresh the data

\* src/main.py <- THE FILE YOU RUN — orchestrates everything



\---



\## How to Run



1\. Open terminal in the project folder.

2\. Fetch data:

&#x20;  py -m scripts.fetch\_live\_data

3\. Run forecast:

&#x20;  py -m src.main

