# to run 
# import requirements
# pip install -r ./requirements.txt
# run the command
# python .\extractHTMLTable2csv.py -i <Input File Path> -o <Output File Pah>


import pandas as pd
import argparse

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Convert First HTML table in file to CSV')
    
    parser.add_argument('-i', '--input', help='Input File Path', required=True)
    parser.add_argument('-o', '--output', help='Output File', required=True)
    args = parser.parse_args()

    input = args.input
    output = args.output

    df = pd.read_html(input)
    df[0].to_csv(output, index=False)