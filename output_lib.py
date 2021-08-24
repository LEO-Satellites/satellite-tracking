import pandas as pd

def output_format(
    data_frame:'PandasDataFrame',
    file_name:'str',
    simple:'bool',
    output_directory:'str'='./output/output_files/'):
    """
    INPUTS
        data_frame:
        file_name:
        simple:
        output_directory:
        save:

    OUTPUTS
        data_frame:
    """
    ############################################################################
    data_frame = data_frame.dropna()
    ############################################################################
# [['satellite', 'date[UT]', 'time[UT]', 'SatRA[hr]', 'SatDEC[deg]']]
    # columns_df = ['satellite',
    #     'date[UT]', 'time[UT]', 'RA[hh:mm:ss]', 'DEC[hh:mm:ss]']

    if not simple:
        data_frame.to_csv(
            f"{output_directory}/{file_name}.txt",
            sep='\t',
            index=False)

        return data_frame
    ############################################################################
    # data = []

    # satellites = data_frame.satellite.unique()
    #
    # for satellite in satellites:
    #     data.append(data_frame[data_frame.satellite == satellite].sample())
    #
    # data_frame = pd.DataFrame().append(data)

    data_frame = data_frame.drop_duplicates('satellite', keep='first')

    data_frame.to_csv(
        f"{output_directory}/{file_name}.txt",
        sep='\t',
        index=False)

    return data_frame
