import os
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

##############################################################################
def output_format(
    frame: "PandasDataFrame",
    file_name: "str",
    simple: "bool",
    output_directory: "str" = "./output/output_files/",
):
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
    ###########################################################################
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    ###########################################################################
    frame = frame.dropna()
    ###########################################################################
    frame["date[UT]"] = pd.to_datetime(
        frame["date[UT]"] + " " + frame["time[UT]"],
        format="%Y-%m-%d %H:%M:%Ss",
    )

    frame = frame.drop(columns=["time[UT]"])

    sort_time = frame["date[UT]"].sort_values().index

    if not simple:
        frame.iloc[sort_time].to_csv(
            f"{output_directory}/{file_name}.txt", sep="\t", index=False
        )

        return frame
    ############################################################################
    frame = frame.drop_duplicates("satellite", keep="first")
    frame.index = range(frame.shape[0])
    sort_time = frame["date[UT]"].sort_values().index

    frame.iloc[sort_time].to_csv(
        f"{output_directory}/{file_name}.txt", sep="\t", index=False
    )

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
# # Prepare data for DataFrame
# columns_df = ["satellite"]
#
# columns_df = columns_df + [
#     header.strip() for header in column_headers.split(",")
# ]
# # all columns nan except the satellite column
# orbital_library_crash = [np.nan for _ in columns_df[:-1]]
# ############################################################################
# data_crash_satellites = []
# data_simple_crash_satellites = []
# visible_satellites = []
#
# for satellite in results:
#
#     if satellite == None:
#
#         satellite_name = ["crash"]
#         data_crash_satellites.append(
#             satellite_name + orbital_library_crash
#         )
#         data_simple_crash_satellites.append(
#             satellite_name + orbital_library_crash[:4]
#         )
#     else:
#
#         visible_satellites.append(satellite)
# ############################################################################
# # Prepare visible satellites data frame
# data_visible_satellites = []
# data_simple_visible_satellites = []
#
# for visible in visible_satellites:
#
#     for visible_ in visible:
#
#         [satellite, data, data_simple] = visible_
#         data_visible_satellites.append([satellite] + data)
#         data_simple_visible_satellites.append([satellite] + data_simple)
# ############################################################################
# data_output_directory = parser.get("directories", "data_output")
#
# if not os.path.exists(data_output_directory):
#     os.makedirs(data_output_directory)
# ############################################################################
# # create DataFrame all data
# data_df = data_visible_satellites + data_crash_satellites
# observations_df = pd.DataFrame(columns=columns_df, data=data_df)
#
# details_name = parser.get("names", "complete")
#
# observations_df = output_format(
#     frame=observations_df,
#     file_name=details_name,
#     simple=False,
#     output_directory=data_output_directory,
# )
# ############################################################################
# # create DataFrame simple data
# columns_df = [
#     "satellite",
#     "date[UT]",
#     "time[UT]",
#     "RA[hh:mm:ss]",
#     "DEC[hh:mm:ss]",
# ]
#
# data_df = data_simple_visible_satellites  # + data_simple_crash_satellites
#
# visible_df = pd.DataFrame(columns=columns_df, data=data_df)
#
# visible_name = parser.get("names", "simple")
#
# observations_df = output_format(
#     frame=visible_df,
#     file_name=visible_name,
#     simple=True,
#     output_directory=data_output_directory,
# )
# # Modify output such I only use the df with all data :)
# ################################################################################
