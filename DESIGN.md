---
title: "Design of Simulating Future Portfolio Returns"
author: "Emma Shauab"
date: "2019-5-16"
output:
  pdf_document: default
  html_document: default
---

### Argument setup
The program sets up the argument parser and parses the arguments which enabled to program to run from the command line argument. This gives the user control over the simulation parameters and the output format.

### Data
I downloaded the data in my local directory for testing, but the the program can download the data directly from the St Louis Federal Reserve Bank. The program reads the data as CSV; the original document represents missing values with `.`, so these are replaced, and the columns are given the correct timestamp and float formats.

### Filter the data to only include observations between start_date and end_date
By using the `if` statement against the supplied date arguments, the program filters data so that it's only in between the start and end date of the data that the user can supply with the command line arguments.


### Ensure there are a reasonable number of observations for yearly bootrstrap samples
The program results would not be meaningful if a very small range of data is used (e.g. only 2 years), so a message will be given if there is not enough data.

### Remove NaN observations
The program removes all the `NaN` so that the yearly returns can be calculated on the samples.


###  Create one draw of yearly return
The `sample_yearly_return` function takes the input data draws a start and end date that spans a year. This is used as one possible yearly return. Internally the functions checks to ensure that the date range chosen includes a full year. If the dates fall on a weekend or day the market wasn't open, it will chose the closest dates inside the range. The program uses "pandas" data frames for collecting the date and return information and to select the relevant data.

### Simualte one trial
The `run_trial` function simulates one possible future realization out to the `num_years` that the user requests. This works by constructing a sequence of returns from repeated calls to `sample_yearly_return`.
    
### Simulate growth of a portfolio using past data
The `run_trials` function then repeats calls to `run_trial` the specified number `num_trials`. Since any individual simulated future return path is highly uncertain, many results are needed to give a good estimate of actual future returns and to determine possible variability. The main work of the program is now done here, and the output data frame can be used for analysis.


### Create a DataFrame with median, upper, and lower returns
The `build_confidence_df` function takes all the simulation results and calculates the median return path as well as the upper and lower quantiles. The quantiles can be specified by the user, so this allows for narrower or wider ranges if the user wants control over the uncertainty. The data frame that the function builds can now be used for plotting.


### Run the simulation
In this stage simulation will run with the given arguments and output an image file, CSV file or image of a graph by default. If the seed was set, the program will be fully reproducible. After the simulation is ran the program unstacks the data in order to print out the ending results. The program also prints out the final balance amounts and will write the full results to file and the graph to an image file if the user supplied the corresponding arguments. The "seaborn" package is used for creating the graph of the simulation results.

