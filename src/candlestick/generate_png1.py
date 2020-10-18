import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import pandas as pd
import uuid

from mplfinance.original_flavor import candlestick2_ochl

PROJECT_PATH = '/home/ubuntu/work/candlestick/'
OUTPUT_PATH = '/home/ubuntu/work/candlestick/'

GROUP_SIZE = 12
CONVOLUSION_SIZE =5

BUY = 0
SELL = 1


def clean_dirs(output):
    for dirs in output:
        for d in dirs:
            print('Handling:', d)
            shutil.rmtree(d, ignore_errors=True)
            os.makedirs(d)

def process_file(filename, start_offset=0, max_count=None):
    f = os.path.basename(filename).replace('.csv', '')
    output = [
        (
            os.path.join(OUTPUT_PATH, 'data', 'output', f, 'training', 'buy'),
            os.path.join(OUTPUT_PATH, 'data', 'output', f, 'training', 'sell')
        ),
        (
            os.path.join(OUTPUT_PATH, 'data', 'output', f, 'validation', 'buy'),
            os.path.join(OUTPUT_PATH, 'data', 'output', f, 'validation', 'sell')
        ),
        (
            os.path.join(OUTPUT_PATH, 'data', 'output', f, 'test', 'buy'),
            os.path.join(OUTPUT_PATH, 'data', 'output', f, 'test', 'sell')
        ),
    ]

    clean_dirs(output)

    df = pd.read_csv(filename, index_col='Date')

    df.index = pd.to_datetime(df.index)
    df.sort_values(by='Date', ascending=True, inplace=True)

    for i in range(len(df)-GROUP_SIZE):
        if i <= start_offset:
            continue

        if i % 20 == 0:
            print('Processed', i, 'entries')

        label, df0 = df.iloc[i], df[i+1:i+GROUP_SIZE+1]

        fig = plt.figure(num=1, figsize=(3, 3), dpi=50, facecolor='w', edgecolor='k')
        
        dx = fig.add_subplot()
        # Also try: width = 0.4, alpha = 1
        candlestick2_ochl(dx, df0['Open'], df0['Close'], df0['High'], df0['Low'], width=1.5, colorup='g', colordown='r', alpha=0.5)
        plt.autoscale()
        
        plt.plot(df0['Close'].rolling(5).mean().reset_index().drop('Date', axis=1).dropna(), color="blue", linewidth=10, alpha=0.5)
        
        plt.axis('off')

        if df0.iloc[0]['Close']  > label['Close']:
            idx = SELL
        else:
            idx = BUY

        p = np.random.rand()
        if p > 0.95:
            dir_idx = 2
        elif p < 0.19:
            dir_idx = 1
        else:
            dir_idx = 0

        jpg_name = os.path.join(output[dir_idx][idx], '{i}.{uuid}.png'.format(i=i, uuid=uuid.uuid4()))

        plt.savefig(jpg_name, bbox_inches='tight')

        plt.cla()
        plt.clf()

        if i == max_count: 
            print('Done. Total', i, 'entries')
            break

        if os.path.exists(os.path.join(OUTPUT_PATH, 'data', 'stop')):
            print('Stopped. Total', i, 'entries')
            break

    print('completed')
