import numpy as np
from numpy import sin, cos, arccos
from datetime import datetime
from constants import LATITUDE, LONGITUDE
from pprint import pprint as pp
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import medfilt
from scipy.ndimage.filters import convolve

def angle_of_incidence(latitude,declination_angle,panel_elevation_angle,panel_azimuth_angle,hour_angle):
    # theta --> angle of incidence on panel
    angle_of_incidence = np.degrees(arccos((
        sin(latitude)*sin(declination_angle)*cos(panel_elevation_angle)
        - cos(latitude)*sin(declination_angle)*sin(panel_elevation_angle)*cos(panel_azimuth_angle)
        + cos(latitude)*cos(declination_angle)*cos(hour_angle)*cos(panel_elevation_angle)*cos(panel_azimuth_angle)
        + cos(declination_angle)*sin(hour_angle)*sin(panel_elevation_angle)*sin(panel_azimuth_angle)
    )))
    # angle_of_incidence = 
    return angle_of_incidence

# def current_date_info(current_date)

def declination_angle(day_of_year):
    # sigma
    declination_angle = 23.45 * sin( (360/365)*(284+day_of_year) )
    return declination_angle
    
# def date_of_year(date):
#     day_of_year = datetime.now().timetuple().tm_yday
    

# def hour_angle(time_of_day,mins_from_solar_noon):
def hour_angle(current_datetime):
    # finding h --> hour angle
    solar_noon = datetime(current_datetime.year,current_datetime.month,current_datetime.day,12)
    if current_datetime >= solar_noon:
        mins_from_solar_noon = (current_datetime - solar_noon).seconds/60
        c = +1
    else:
        mins_from_solar_noon = (solar_noon - current_datetime).seconds/60
        c = -1
    h = c*0.25*(mins_from_solar_noon)
    return h

# def get_db(db_path):
#     df = pd.read_csv(db_path)


if __name__ == '__main__':
    df = pd.read_csv('s3616479.csv')

    row_num = 7746 # 7740 # 12 # 7739 11    input=excel-2 || 7740=7742-2
    panel_elevation_angle = 45
    panel_azimuth_angle = 0

    csv_row = df.iloc[row_num,[0,1]]
    datetime_string = csv_row[0] + ' ' + csv_row[1]
    datetime_format = "%m/%d/%y %H:%M:%S"
    current_datetime = datetime.strptime(datetime_string, datetime_format)
    # pp(current_datetime)
    n_days = current_datetime.timetuple().tm_yday
    # pp(n_days)
    
    declination_angle = declination_angle(n_days)
    hour_angle = hour_angle(current_datetime)
    # pp(hour_angle)
    
    # aoi = angle_of_incidence(LATITUDE,declination_angle,panel_elevation_angle,panel_azimuth_angle,hour_angle)
    # pp(aoi)

    # mylist_a = []
    # for j in range (0,180,2):
    #     panel_elevation_angle = np.radians(j)
    #     mylist_b = []
    #     for i in range(0,360,2):
    #         panel_azimuth_angle = np.radians(i)
    #         aoi = angle_of_incidence(LATITUDE,declination_angle,panel_elevation_angle,panel_azimuth_angle,hour_angle)
    #         # print(i,aoi)
    #         # mylist_a.append(i)
    #         mylist_b.append(aoi)
    #     print(j,min(mylist_b))
    #     mylist_a.append(min(mylist_b))

    a_def = 1 # must cleanly divide 360
    e_def = 1 # must cleanly divide 360

    aoi_matrix = np.ndarray((int(360/a_def),int(180/e_def)))

    for i, azimuth_angle in enumerate(range(0,360,a_def)):
        panel_elevation_angle = np.radians(azimuth_angle)
        for j, elevation_angle in enumerate(range(0,180,e_def)):
            panel_azimuth_angle = np.radians(elevation_angle)
            aoi = angle_of_incidence(LATITUDE,declination_angle,panel_elevation_angle,panel_azimuth_angle,hour_angle)
            # aoi_matrix[azimuth_angle,elevation_angle] = aoi
            aoi_matrix[i,j] = aoi

    # pp(aoi_matrix)

    min_aoi_per_azimuth = np.ndarray((int(360/a_def),2))
    for i, row in enumerate(aoi_matrix):
        min_aoi_per_azimuth[i] = [np.where(row==np.nanmin(row))[0],np.nanmin(row)]
    pp(min_aoi_per_azimuth)
    # pp(min_aoi_list) # for each azimuth angle, have a tuple containing the minimum aoi and the elevation at which than minimum is acheived
        # hence something like min_aoi_per_azimuth_increment = [(46,2.5),(48,3.53), ... ]  with a size of (360/def_a, 2)

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    
    ax1.plot(min_aoi_per_azimuth[:,0], label="Elevation", color='orange') # convolve(min_aoi_per_azimuth[:,0],np.full((9,),1/9))
    ax2.plot(min_aoi_per_azimuth[:,1], label="Minimum AOI")

    ax1.set_xlabel('Panel azimuth')
    ax1.set_ylabel('Elevation')
    ax2.set_ylabel('Minimum AOI')

    plt.legend()
    plt.show()
