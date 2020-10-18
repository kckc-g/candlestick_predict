import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import pandas as pd
import uuid

from mplfinance.original_flavor import candlestick2_ochl

def process_dataframe(df, output_dirname, window_length=12, testing_percent=0.05, validation_percent=0.2, remove_existing_files=True):
    """Process dataframe that contains OCHL data to generate candlestick diagram

    Assumes data can be sorted in ascending order by index, and column names are:
    ['Open', 'Close', 'High', 'Low']

    Withhold `testing_percent`% data for independent data

    Remaining is then split up into validation and trianing, according to `validation_percent`
    (defaults to 20/80 split)
    """
    assert window_length > 0, 'Candlestick graph window length must be greater than 0'

    validation_p = 1 - (1 - testing_percent) * validation_percent
    
    test_dir = os.path.join(output_dirname, 'test')
    valid_dir = os.path.join(output_dirname, 'validation')
    train_dir = os.path.join(output_dirname, 'training')

    if remove_existing_files:
        for d in [test_dir, valid_dir, train_dir]:
            shutil.rmtree(d, ignore_errors=True)
            os.makedirs(os.path.join(d, 'buy'))
            os.makedirs(os.path.join(d, 'sell'))

    def _process(indices, df):
        return processed

    df = df.sort_index(ascending=True)

    fig = plt.figure(num=1, figsize=(3, 3), dpi=50, facecolor='w', edgecolor='k')

    for i in range(len(df)-(window_length+1)):
        if i % 100 == 0:
            print('Processed', i, 'entries - ', dt.datetime.now())

        df0, t1 = df.iloc[i:i+window_length], df.iloc[i+window_length]

        p = np.random.rand()
        if p < testing_percent:
            image_dir = test_dir
        elif p > validation_p:
            image_dir = valid_dir
        else:
            image_dir = train_dir

        image_filename = '{i}.{uuid}.png'.format(i=i, uuid=uuid.uuid4())
        if df0.iloc[-1]['Close'] > t1['Close']:
            image_filename = os.path.join(image_dir, 'sell', image_filename)
        else:
            image_filename = os.path.join(image_dir, 'buy', image_filename)

        candlestick2_ochl(fig.gca(),
                          df0['Open'],
                          df0['Close'],
                          df0['High'],
                          df0['Low'],
                          width=1.5,
                          colorup='g',
                          colordown='r',
                          alpha=0.5)

        plt.autoscale()

        if False:
            sma = pd.Series(series_close).rolling(sma_days).mean().reset_index(drop=True).dropna()
            plt.plot(sma, color="blue", linewidth=10, alpha=0.5)

        plt.axis('off')
        plt.savefig(image_filename, bbox_inches='tight')

        plt.clf()


def process_csv_file(filename, output_dirname):
    print('Processing -', filename)

    sub_folder = os.path.basename(filename).replace('.csv', '')

    df = pd.read_csv(filename, index_col='Date')

    df.index = pd.to_datetime(df.index)
    df.sort_values(by='Date', ascending=True, inplace=True)

    process_dataframe(df, os.path.join(output_dirname, sub_folder))

    print('Completed')

