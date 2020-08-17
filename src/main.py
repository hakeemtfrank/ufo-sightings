# import libraries
import numpy as np 
import pandas as pd


def load_ufo_data(input_path='../data/scrubbed.csv', export=False, export_path='../data/ufo_sightings.csv'):
    ''' 
    This function processes data from `../data/scrubbed.csv` to be used in the web map.
    To download the data from its original source, go to data/ and run 
    `bash fetch_data.sh`.

    Date columns are converted to datetime for further analysis in Python.

    Returns:
        ufo_data (pandas DataFrame): Processed UFO sighting data
    '''

    colnames = ['datetime','city','state','country','shape','duration (seconds)','duration (hours/min)','comments','date posted','latitude','longitude']
    # load data
    ufo_data = pd.read_csv(input_path, low_memory = False, na_values = ['UNKNOWN','UNK'], 
                            na_filter = True, skip_blank_lines = True, names=colnames) 

    # choose columns based on our questions
    cols = ['datetime', 'city', 'state', 'country', 'shape', 'duration (seconds)',
            'comments', 'date posted', 'latitude', 'longitude']

    # narrow down columns
    ufo_data = ufo_data[cols]

    # convert lat / long to float
    ufo_data['latitude'] = pd.to_numeric(ufo_data['latitude'],errors = 'coerce')
    ufo_data['longitude'] = pd.to_numeric(ufo_data['longitude'], errors='coerce')

    # clean illegal dates and convert to dt
    ufo_data['datetime'] = ufo_data['datetime'].str.replace('24:00', '00:00')
    ufo_data['datetime'] = pd.to_datetime(ufo_data['datetime'], format='%m/%d/%Y %H:%M')

    # year for slider in ArcGIS
    ufo_data['year'] = ufo_data['datetime'].dt.year

    # export if true
    if export == True:
        ufo_data.to_csv(export_path, index=False)
    
    return ufo_data

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Path to scrubbed.csv.')
    parser.add_argument('-i', '--input_path', default='../data/scrubbed.csv', required=False)
    parser.add_argument('-o', '--output_path', default='../data/ufo_sightings.csv', required=False)
    args = parser.parse_args()

    # if run as a script, save the data to a .csv in data.
    print("Processing data..\n")

    load_ufo_data(input_path=args.input_path, export_path=args.output_path, export=True)

    print("Done!")