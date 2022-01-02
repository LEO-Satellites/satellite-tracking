###############################################################################
# observatory - abbreviated observatory name
# name - full observatory name
# longitude - observatory longitude in degrees *west*
# latitude - observatory latitude in degrees
# altitude - observatory altitude in meters above sea level
# tz - time zone, number of hours *west* of Greenwich
###############################################################################
# Details taken from the IDL script observatories.pro
###############################################################################
observatories = {
    "kpno": {
        "name": "Kitt Peak National Observatory",
        "longitude": [111, 36.0],
        "latitude": [31, 57.8],
        "altitude": 2120.0,
        "tz": 7,
    },
    "ctio": {
        "name": "Cerro Tololo Interamerican Observatory",
        "longitude": 70.815,
        "latitude": -30.16527778,
        "altitude": 2215.0,
        "tz": 4,
    },
    "lasilla": {
        "name": "European Southern Observatory, La Silla",
        "longitude": [70, 43.8],
        "latitude": [-29, 15.4],
        "altitude": 2347.0,
        "tz": 4,
    },
    "lick": {
        "name": "Lick Observatory",
        "longitude": [121, 38.2],
        "latitude": [37, 20.6],
        "altitude": 1290.0,
        "tz": 8,
    },
    "mmto": {
        "name": "MMT Observatory",
        "longitude": [110, 53.1],
        "latitude": [31, 41.3],
        "altitude": 2600.0,
        "tz": 7,
    },
    "cfht": {
        "name": "Canada-France-Hawaii Telescope",
        "longitude": [155, 28.3],
        "latitude": [19, 49.6],
        "altitude": 4215.0,
        "tz": 10,
    },
    "lapalma": {
        "name": "Roque de los Muchachos, La Palma",
        "longitude": [17, 52.8],
        "latitude": [28, 45.5],
        "altitude": 2327,
        "tz": 0,
    },
    "mso": {
        "name": "Mt. Stromlo Observatory",
        "longitude": [210, 58, 32.4],
        "latitude": [-35, 19, 14.34],
        "altitude": 767,
        "tz": -10,
    },
    "sso": {
        "name": "Siding Spring Observatory",
        "longitude": [210, 56, 19.70],
        "latitude": [-31, 16, 24.10],
        "altitude": 1149,
        "tz": -10,
    },
    "aao": {
        "name": "Anglo-Australian Observatory",
        "longitude": [210, 56, 2.09],
        "latitude": [-31, 16, 37.34],
        "altitude": 1164,
        "tz": -10,
    },
    "mcdonald": {
        "name": "McDonald Observatory",
        "longitude": 104.0216667,
        "latitude": 30.6716667,
        "altitude": 2075,
        "tz": 6,
    },
    "mtbigelow": {
        "name": "Catalina Observatory: 61 inch telescope",
        "longitude": [110, 43.9],
        "latitude": [32, 25.0],
        "altitude": 2510.0,
        "tz": 7,
    },
    "dao": {
        "name": "Dominion Astrophysical Observatory",
        "longitude": [123, 25.0],
        "latitude": [48, 31.3],
        "altitude": 229.0,
        "tz": 8,
    },
    "mdm": {
        "name": "Michigan-Dartmouth-MIT Observatory",
        "longitude": [111, 37.0],
        "latitude": [31, 57.0],
        "altitude": 1938.5,
        "tz": 7,
    },
    "nov": {
        "name": "National Observatory of Venezuela",
        "longitude": [70, 52.0],
        "latitude": [8, 47.4],
        "altitude": 3610,
        "tz": 4,
    },
    "bao": {
        "name": "Beijing XingLong Observatory",
        "longitude": [242, 25.5],
        "latitude": [40, 23.6],
        "altitude": 950.0,
        "tz": -8,
    },
    "keck": {
        "name": "W. M. Keck Observatory",
        "longitude": [155, 28.7],
        "latitude": [19, 49.7],
        "altitude": 4160.0,
        "tz": 10,
    },
    "loiano": {
        "name": "Bologna Astronomical Observatory, Loiano - Italy",
        "longitude": [348, 39, 58],
        "latitude": [44, 15, 33],
        "altitude": 785.0,
        "tz": -1,
    },
    "apo": {
        "name": "Apache Point Observatory",
        "longitude": [105, 49.2],
        "latitude": [32, 46.8],
        "altitude": 2798.0,
        "tz": 7,
    },
    "vbo": {
        "name": "Vainu Bappu Observatory",
        "longitude": 281.1734,
        "latitude": 12.57666,
        "altitude": 725.0,
        "tz": -5.5,
    },
    "flwo": {
        "name": "Whipple Observatory",
        "longitude": [110, 52, 39],
        "latitude": [31, 40, 51.4],
        "altitude": 2320.0,
        "tz": 7,
    },
    "oro": {
        "name": "Oak Ridge Observatory",
        "longitude": [71, 33, 29.32],
        "latitude": [42, 30, 18.94],
        "altitude": 184.0,
        "tz": 5,
    },
    "saao": {
        "name": "South African Astronomical Observatory",
        "longitude": [339, 11, 21.5],
        "latitude": [-32, 22, 46],
        "altitude": 1798.0,
        "tz": -2,
    },
    "bosque": {
        "name": "Estacion Astrofisica Bosque Alegre, Cordoba",
        "longitude": [64, 32, 45],
        "latitude": [-31, 35, 54],
        "altitude": 1250,
        "tz": 3,
    },
    "rozhen": {
        "name": "National Astronomical Observatory Rozhen - Bulgaria",
        "longitude": [335, 15, 22],
        "latitude": [41, 41, 35],
        "altitude": 1759,
        "tz": -2,
    },
    "irtf": {
        "name": "NASA Infrared Telescope Facility",
        "longitude": 155.471999,
        "latitude": 19.826218,
        "altitude": 4168,
        "tz": 10,
    },
    "bgsuo": {
        "name": "Bowling Green State Univ Observatory",
        "longitude": [83, 39, 33],
        "latitude": [41, 22, 42],
        "altitude": 225.0,
        "tz": 5,
    },
    "ca": {
        "name": "Calar Alto Observatory",
        "longitude": [2, 32, 46.5],
        "latitude": [37, 13, 25],
        "altitude": 2168,
        "tz": -1,
    },
    "fmo": {
        "name": "Fan Mountain Observatory",
        "longitude": [78, 41, 34],
        "latitude": [37, 52, 41],
        "altitude": 556,
        "tz": 5,
    },
    "whitin": {
        "name": "Whitin Observatory, Wellesley College",
        "longitude": 71.305833,
        "latitude": 42.295,
        "altitude": 32,
        "tz": 5,
    },
    "tubitak": {
        "name": "TUBITAK National Observatory, Turkey",
        "longitude": [329, 39, 52],
        "latitude": [36, 49, 27],
        "altitude": 2490.0,
        "tz": -3,
    },
    "lco": {
        "name": "Las Campanas Observatory",
        "longitude": [70, 42.1],
        "latitude": [-29, 0.2],
        "altitude": 2282,
        "tz": 4,
    },
    "ekar": {
        "name": "Mt. Ekar 182 cm. Telescope",
        "longitude": [348, 25, 7.92],
        "latitude": [45, 50, 54.92],
        "altitude": 1413.69,
        "tz": -1,
    },
    "lowell": {
        "name": "Lowell Observatory",
        "longitude": [111, 32.1],
        "latitude": [35, 5.8],
        "altitude": 2198.0,
        "tz": 7,
    },
    "casleo": {
        "name": "Complejo Astronomico El Leoncito, San Juan",
        "longitude": [69, 18, 0],
        "latitude": [-31, 47, 57],
        "altitude": 2552,
        "tz": 3,
    },
    "mgio": {
        "name": "Mount Graham International Observatory",
        "longitude": [109, 53, 31.25],
        "latitude": [32, 42, 4.69],
        "altitude": 3191.0,
        "tz": 7,
    },
    "lna": {
        "name": "Laboratorio Nacional de Astrofisica - Brazil",
        "longitude": 45.5825,
        "latitude": [-22, 32, 4],
        "altitude": 1864.0,
        "tz": 3,
    },
    "spm": {
        "name": "Observatorio Astronomico Nacional, San Pedro Martir",
        "longitude": [115, 29, 13],
        "latitude": [31, 1, 45],
        "altitude": 2830.0,
        "tz": 7,
    },
    "ckoir": {
        "name": "Ckoirama Observatory, Universidad de Antofagasta, Chile",
        "longitude": 69.93058889,
        "latitude": -24.08913333,
        "altitude": 966.0,
        "tz": 4,
    },
    "lmo": {
        "name": "Leander McCormick Observatory",
        "longitude": [78, 31, 24],
        "latitude": [38, 2, 0],
        "altitude": 264,
        "tz": 5,
    },
    "palomar": {
        "name": "The Hale Telescope",
        "longitude": [116, 51, 46.80],
        "latitude": [33, 21, 21.6],
        "altitude": 1706.0,
        "tz": 8,
    },
    "quynhon": {
        "name": "The Quy Nhon Observatory",
        "longitude": 250.786994,
        "latitude": 13.71863,
        "altitude": 5.0,
        "tz": -7,
    },
    "CBNUO": {
        "name": "ChungBuk National University Observatory",
        "longitude": 232.524644889,
        "latitude": 36.7815,
        "altitude": 86.92,
        "tz": -9,
    },
    "ouka": {
        "name": "Oukaimeden observatory",
        "longitude": 7.866,
        "latitude": 31.206389,
        "altitude": 2700.0,
        "tz": -1,
    },
}

###############################################################################
def get_observatory_data(observatories: "dict") -> "dict":
    """
    Process observatory data to have in the format ???

    PARAMETERS

        observatories: A dictionary with the structure
            {
                "kpno":
                {
                    "name": "Kitt Peak National Observatory",
                    "longitude": [111, 36.0],
                    "latitude": [31, 57.8],
                    "altitude": 2120.0,
                    "tz": 7,
                },
            ...
            }

    OUTPUTS

        Returns dictionary with data converted to ???
    """

    observatories_update = {}
    ###########################################################################
    for name_observatory, data_observatory in observatories.items():

        update_format = {}
        #######################################################################
        for (
            parameter_observatory,
            parameters_values,
        ) in data_observatory.items():
            # parameter_observatory:
            # "name", "longitude", "latitude", "altitude", "tz"
            #  parameters values: longitude and latitude format are
            #     [degree, minute, second] up to 360 to the west

            if type(parameters_values) == list:
                sign = 1  # negative to the west and positive to the east
                update_format[parameter_observatory] = 0
                ###############################################################
                for idx, parameter in enumerate(parameters_values):

                    # parameter will be in degrees, minutes and seconds
                    # idx=0 -> degrees
                    # idx=1 -> minutes
                    # idx=2 -> seconds
                    # maybe a lamda function with map?
                    if parameter < 0:
                        sign = -1
                        parameter = abs(parameter)

                    update_format[parameter_observatory] += parameter / (
                        60 ** idx
                    )
                ###############################################################
                update_format[parameter_observatory] = (
                    sign * update_format[parameter_observatory]
                )

            else:
                update_format[parameter_observatory] = parameters_values

            if parameter_observatory == "longitude":

                if update_format[parameter_observatory] > 180.0:
                    update_format[parameter_observatory] = (
                        360 - update_format[parameter_observatory]
                    )

                else:
                    update_format[parameter_observatory] = -update_format[
                        parameter_observatory
                    ]

        observatories_update[name_observatory] = update_format
    ###########################################################################
    return observatories_update
