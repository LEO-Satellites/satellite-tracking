import pandas as pd

def output_format(
    frame:'PandasDataFrame',
    file_name:'str',
    simple:'bool',
    output_directory:'str'='./output/output_files/'):
    """
    PARAMETERS
        frame:
        file_name:
        simple:
        output_directory:
        save:

    OUTPUTS
        frame:
    """
    ############################################################################
    frame = frame.dropna()
    ############################################################################
    # [['satellite', 'date[UT]', 'time[UT]', 'SatRA[hr]', 'SatDEC[deg]']]
    # columns_df = ['satellite',
    #     'date[UT]', 'time[UT]', 'RA[hh:mm:ss]', 'DEC[hh:mm:ss]']
    frame['date-time[UT]'] = pd.to_datetime(
        frame['date[UT]'] + ' ' + frame['time[UT]'],
        format='%Y-%m-%d %H:%M:%Ss'
        )

    frame.drop(columns=['date[UT]', 'time[UT]'])

    sort_time = frame['date-time[UT]'].sort_values().index

    if not simple:
        frame.iloc[sort_time].to_csv(
            f"{output_directory}/{file_name}.txt",
            sep='\t',
            index=False)

        return frame
    ############################################################################
    frame = frame.drop_duplicates('satellite', keep='first')
    frame.index = range(frame.shape[0])
    sort_time = frame['date-time[UT]'].sort_values().index

    frame.iloc[sort_time].to_csv(
        f"{output_directory}/{file_name}.txt",
        sep='\t',
        index=False)

    return frame
    ############################################################################
    # observing_time = np.empty(len(visible_satellites))

   #  for idx, visible in enumerate(visible_satellites):

   #      [satellite, str, str_simple] = visible

   #      obs_time = str_simple.split('\t')[1].split(':')

   #      hours = float(obs_time[0])
    #     if hours < 3:
    #         hours += 24

   #      minutes = float(obs_time[1])/60.
    #     seconds = float(obs_time[2][:-1])/3600.

   #      obs_time = hours + minutes + seconds

   #      observing_time[idx] = obs_time
################################################################################

    # obs_time_sort_ids = np.argsort(observing_time)

    # for sort_id in obs_time_sort_ids:

    #     [satellite, str, str_simple] = visible_satellites[sort_id]

    #     with open(f'{output_dir}/{output_fname}.txt',
     #              'a') as file:
     #        file.write(f'{satellite}\n{str}\n')

    #     with open(f'{output_dir}/{output_fname_simple}.txt',
     #              'a') as file_simple:
     #        file_simple.write(f'{satellite}\n{str_simple}\n')
################################################################################
