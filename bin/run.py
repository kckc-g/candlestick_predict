from candlestick import generate_png

def main():
    generate_png.process_csv_file(filename='/home/ubuntu/work/candlestick/data/input/eurusd.csv', output_dirname='/home/ubuntu/work/candlestick/data/output')
    generate_png.process_csv_file(filename='/home/ubuntu/work/candlestick/data/input/xausd.csv',  output_dirname='/home/ubuntu/work/candlestick/data/output')

if __name__ == '__main__':
    main()

