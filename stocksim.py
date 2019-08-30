"""
Simulate future returns for a portfolio
"""
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='stocksim')
    parser.add_argument('-s', "--start_date", help="The Start Date format YYYY-MM-DD (Inclusive)", required=False, type=str)
    parser.add_argument('-e', "--end_date", help="The End Date format YYYY-MM-DD (Inclusive)", required=False, type=str)
    parser.add_argument('-n', "--num_years", help="The number of years format xx (Inclusive)", required=False, type=int, default=10)
    parser.add_argument("--start_amount", help="Initial starting amount", default=100, required=False, type=int)
    parser.add_argument('-t', "--num_trials", help="Number of simulation trials", default=1000, required=False, type=int)
    parser.add_argument("--seed", help="Seed for reproducibility", required=False, type=int)
    parser.add_argument("--quantile", help="Quatile limits for the graph", default=0.05, required=False, type=float)
    parser.add_argument("--output_image", help="Outputs graph to image file", required=False, type=str)
    parser.add_argument("--output_csv", help="Output results to CSV file", required=False, type=str)

    args = parser.parse_args()

    if args.num_years < 1:
        print('num_years must be at least 1')
        exit
    if args.start_amount <= 0:
        print('start_amount must be greater than zero')
        exit
    if args.quantile < 0 or args.quantile > 1:
        print('quantile must not be less than zero or greater than one')
        exit
    start_date = args.start_date
    end_date = args.end_date
    start_amount = args.start_amount
    num_trials = args.num_trials
    num_years = args.num_years
    quantile = args.quantile
    seed = args.seed
    output_csv = args.output_csv
    output_image = args.output_image
    if start_date:
        print(f"Using data starting in {start_date}")
    if end_date:
        print(f"Using data ending in {end_date}")

    print(f"Simulating {num_years} future years")


    # Read the data from the St Louis Federal Reserve
    data_url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=WILL5000INDFC'
    # During debug and development, a local location could be used for faster read
    #data_url = '/home/emma/Downloads/WILL5000INDFC.csv'
    data = pd.read_csv(data_url, na_values='.')

    # Filter the data to only include observations between start_date and end_date
    if start_date:
        data = data.loc[data['DATE'] >= start_date, :]
    if end_date:
        data = data.loc[data['DATE'] <= end_date, :]


    # Ensure there are a reasonable number of observations for yearly bootrstrap samples
    num_obs = data.shape[0]
    if num_obs < 1000:
        print('Bootstrap samples require at least 1000 observations for any reliability')
        exit

    # Remove NaN observations
    data = data.loc[~data['WILL5000INDFC'].isnull(), :]

    # Convert dates to timestamp objects
    data['DATE'] = data['DATE'].astype('datetime64[D]')

    def sample_yearly_return(data):
        """
        Create one draw of yearly return
        :param data: a DataFrame with DATE and WILL5000INDFC
        """
        # Choose a random start date
        start_date = data['DATE'].sample(1).iloc[0]
        end_date = start_date + pd.Timedelta('365d')
        max_date = data['DATE'].max()

        # If random start date is less than one year from end of dataset, draw again
        if end_date > max_date:
            return sample_yearly_return(data)
        else:
            # Protect against start/end date landing on weekend of holiday
            subset_data = data.loc[(data['DATE'] >= start_date) & (data['DATE'] <= end_date),
                                   'WILL5000INDFC']
            end_value = subset_data.tail(1).iloc[0]
            start_value = subset_data.head(1).iloc[0]
            yearly_return = float(end_value) / start_value
            return yearly_return

    def run_trial(data, start_amount, num_years):
        """
        Simulate one possible return path for the investment
        :param data: the data
        :param start_amount: the starting balance
        :param num_years: the number of years to simulate
        """
        new_balance = start_amount
        running_balance = [start_amount]
        for _ in range(num_years):
            new_balance *= sample_yearly_return(data)
            running_balance.append(new_balance)
        return running_balance

    def run_trials(data, start_amount, num_years, num_trials):
        """
        Simulate growth of a portfolio using past data
        :param data: a pandas DataFrame with past market data
        :param start: the starting balance
        :param num_years: the number of years to simualate
        :param num_trials: the number of Monte Carlo trials
        """
        df = pd.DataFrame()
        for num in range(num_trials):
            realization = run_trial(data, start_amount, num_years)
            col_name = f'trial_{num}'
            df[col_name] = realization
        return df

    def build_confidence_df(df, q=0.05):
        """
        Create a DataFrame with median, upper, and lower returns
        :parma df: a DataFrame with simulation results
        :param q: the quantile for upper and lower intervals
        """
        years = df.index
        median = df.median(axis=1)
        median_df = pd.DataFrame({'year': years, 'balance': median, 'percentile': 'median'})

        lower = df.quantile(q=q, axis=1)
        lower_df = pd.DataFrame({'year': years, 'balance': lower, 'percentile': 'lower'})

        upper = df.quantile(q=1 - q, axis=1)
        upper_df = pd.DataFrame({'year': years, 'balance': upper, 'percentile': 'upper'})

        quantile_df = pd.concat([lower_df, median_df, upper_df])
        return quantile_df

    # Set the seed if it was supplied
    if seed:
        np.random.seed(seed)

    # Run the simulation
    results = run_trials(data=data, start_amount=start_amount, num_years=num_years, num_trials=num_trials)

    # Unstack the data for plotting
    quantile_df = build_confidence_df(df=results, q=quantile)

    # Print the ending balance results
    upper_result = round(quantile_df.loc[quantile_df['percentile'] == 'upper', 'balance'].iloc[-1], 2)
    median_result = round(quantile_df.loc[quantile_df['percentile'] == 'median', 'balance'].iloc[-1], 2)
    lower_result = round(quantile_df.loc[quantile_df['percentile'] == 'lower', 'balance'].iloc[-1], 2)

    print(f'The upper {100 - 100 * quantile} quantile end balance is {upper_result}')
    print(f'The median end balance is {median_result}')
    print(f'The lower {100 * quantile} quantile end balance is {lower_result}')

    # Write trial results to file if supplied
    if output_csv:
        results.to_csv(output_csv)

    # Plot the results
    title = f'Simulation of {num_years} years with {num_trials} trials and upper/lower {quantile * 100} quantiles'
    sns_plot = sns.relplot(x='year', y='balance', kind='line', hue='percentile', data=quantile_df)

    # Write graph to image file if supplied, otherwise show picture
    if output_image:
        fig = sns_plot
        fig.savefig(output_image)
    else:
        plt.show()
