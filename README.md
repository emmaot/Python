---
title: "Simulating Future Portfolio Returns"
author: "Emma Shaub"
date: "2019-5-16"
output:
  pdf_document: default
  html_document: default
---




In this project I have designed a program that predicts future returns on a stock market portfolio. This program uses [Monte Carlo](https://en.wikipedia.org/wiki/Monte_Carlo_method) simulations to estimate ranges of possible portfolio outcomes. I have created several arguments that makes the simulation more useful and customizable with the user's needs. A possible use of this program is to simulate how your investment portfolio might grow over time and to see what some of the worst and best-case scenarios are.

![simulation results](results.png)

If you do not give any arguments the program will use the default values. For example:
```
$ python3 stocksim.py 
Simulating 10 future years
The upper 95.0 quantile end balance is 650.79
The median end balance is 290.67
The lower 5.0 quantile end balance is 116.26
```

The raw results can be saved to a CSV file, and the output graph can also be saved to an image file. The data source is the broad Willshire 5000 index from the St Louis Federal Reserve.



##Arguments
### Start Date
By default the program will use all data available (roughly 1970 to present). To provide a start date to exclude some data in your simulation use the `--start_date` argument. For example,
for example:
```
$ python3 stocksim.py --start_date=1985-03-30 --num_years=10 --num_trials=100 
--start_amount=1000
Using data starting in 1985-03-30
Simulating 10 future years
The upper 95.0 quantile end balance is 553.67
The median end balance is 286.95
The lower 5.0 quantile end balance is 122.28

```
### End Date
To provide and end date to your simulation use the `--end-date` argument:
For example:
```
$ python3 stocksim.py --start_date=1999-12-31 --end_date=2010 --num_years=10 --num_trials=100 
--stUsing data starting in 1999-12-31
Using data ending in 2010
Simulating 10 future years
The upper 95.0 quantile end balance is 227.7
The median end balance is 82.8
The lower 5.0 quantile end balance is 29.69
```

Both `--start_date` and `--end_date` can also be used simultaneously to limit the data.

### Number of years
To specify the number of future years to simulate, use the `--num_years` argument; the default is 10 years.

For example:
```
$ python3 stocksim.py --num_years=20 --num_trials=100
Simulating 20 future years
The upper 95.0 quantile end balance is 3319.32
The median end balance is 831.5
The lower 5.0 quantile end balance is 290.66
```
### Start amount
To run your simulation with a different start amount of money use the `--start_amount` argument; the default amount is 100.
For example:
```
$ python3 stocksim.py --num_years=10 --start_amount=300
Simulating 10 future years
The upper 95.0 quantile end balance is 1991.49
The median end balance is 913.12
The lower 5.0 quantile end balance is 351.68
```

### Number of trials
To run your simulation with a specified number of trials use the `--num_trials` argument; the default trial amount is 1000.
For example:
```
$ python3 stocksim.py --start_date=1973 --end_date=1985-02-15 --num_years=20 --num_trials=100 
--start_amount=10000
Using data starting in 1973
Using data ending in 1985-02-15
Simulating 20 future years
The upper 95.0 quantile end balance is 4791.82
The median end balance is 1111.67
The lower 5.0 quantile end balance is 251.41
```
### Seed
To run your simulation with a seed for reproductivity, use the `--seed` argument. The seed fixes the random state so the same result can be produced with multiple calls of the program. Since the program downloads the latest data possible, the `start_date` and `end_date` would also need to be provided if the program runs on different dates.
For example:
```
$ python3 stocksim.py  --num_trials=100  --seed=10
Simulating 10 future years
The upper 95.0 quantile end balance is 578.61
The median end balance is 286.65
The lower 5.0 quantile end balance is 126.92
```
### Quantile
To control the upper, median and lower boundaries in your simulation user the `--quantie` argument. The default quantile is `0.05`.
For example:
```
$ python3 stocksim.py --start_date=1975-12-15 --end_date=2010-08-03 --num_years=20 --num_trial=1000 
--start_amount=100000 --seed=100 --quantile=0.01
Using data starting in 1970
Using data ending in 2010
Simulating 20 future years
The upper 99.0 quantile end balance is 3624994.02
The median end balance is 751039.02
The lower 1.0 quantile end balance is 119914.42
```
### Output the result to image file
To output the graph image to a file, use the `--output_image` argument:
For example:
```
$ python3 stocksim.py --start_date=1970 --end_date=2010 --num_years=20 --num_trial=1000 
--start_amount=100000 --seed=100 --quantile=0.01 --output_image results.png
Using data starting in 1970
Using data ending in 2010
Simulating 20 future years
The upper 99.0 quantile end balance is 3624994.02
The median end balance is 751039.02
The lower 1.0 quantile end balance is 119914.42
```
And find the image in your present directory; in this case it's `results.png`.

### Output the simulation results to CSV file
To output the result to a CSV file use the `--output_csv` argument: 
For example:
```
$ python3 stocksim.py --start_date=1970 --end_date=2010 --num_years=20 --num_trial=1000
--start_amount=100000 --seed=100 --quantile=0.01 --output_csv results.csv
Using data starting in 1970
Using data ending in 2010
Simulating 20 future years
The upper 99.0 quantile end balance is 3624994.02
The median end balance is 751039.02
The lower 1.0 quantile end balance is 119914.42
```
And find the CSV file in your current directory; in this case it's `results.csv`.
