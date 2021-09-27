def get_satellite_from_tle(file_location):
    """Read tle file"""

    satellites_list = []

    with open(f'{file_location}', 'r') as tle:

        lines_tle = tle.readlines()

    for idx, l in enumerate(lines_tle):

        if idx%3==0:
            satellites_list.append(l.strip())

    pass
