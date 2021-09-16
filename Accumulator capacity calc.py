## Cell and module selection
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import trapz
import matplotlib as mpl
import pathlib

working_directory = pathlib.Path(__file__).parent

#Change font size for all figures
mpl.rcParams.update({'font.size': 22})


##Instructions:
#1. Add your speed-time data into the drive cycle sheet of the excel spreadhseet. Make sure this is speed (mph) - time (seconds)
#2. Add your car data in the the car data sheet of the excel spreadhseet 
#3  Run the script.
############################################################################################################################
## speed-time data graph
speed_data = pd.read_excel(working_directory/'Car data.xlsx', sheet_name='drive cycle')

time_s = np.array(speed_data.iloc[0:, 1])
speed_mph = np.array(speed_data.iloc[0:, 0])


plt.figure(figsize=(10, 10))
plt.plot(time_s, speed_mph)
plt.xlabel('Time (seconds)')
plt.ylabel('Speed (mph)')
plt.title('Speed vs Time')
plt.show()
###########################################################################################################################
##Model of forces on car
car_data = pd.read_excel(working_directory/'Car data.xlsx', sheet_name='car data')

speed_ms = np.array(speed_data.iloc[0:, 0]/2.237)  # speed in m/s

#Car parameters
air_den = car_data.iloc[0, 1]  # air density (kg/m3)
fro_area = car_data.iloc[1, 1]  # frontal area (m^2)
roll_res_co = car_data.iloc[2, 1] #Rolling resistance coefficient
car_mass = car_data.iloc[3, 1]  # Total mass of car with driver (kg)
air_speed = car_data.iloc[4, 1]  # assumed 0 for now
track_fric = car_data.iloc[5, 1]  # coefficient of friction of track
motor_eff = car_data.iloc[6, 1]  # Motor efficiency #need to workout
drag_coe = car_data.iloc[7, 1]  # Drag coefficient #need to check
inv_eff = car_data.iloc[8, 1]  # inverter/motor controlled efficiency

#Calculation of aerodynamic drag
# Aerodynamic drag(N)
drag_resis = np.array((air_den*fro_area*drag_coe*(speed_ms)**2)/2)

#Speed (m/s) vs Time (s) graoh

#plt.figure(figsize=(100, 4))
#plt.xticks(np.arange(min(time_s), max(time_s)+1, 5))
plt.figure(figsize=(10, 10))
plt.plot(time_s, speed_ms)
#plt.figure(figsize=(6, 4))
#plt.xticks(np.arange(min(time_s), max(time_s)+1, 5))
plt.xlabel('Time (seonds)')
plt.ylabel('Speed (m/s)')
plt.title('Speed vs Time')
plt.show()


# Aerodynamic drag resistance graph
plt.figure(figsize=(10, 10))
plt.plot(time_s, drag_resis)
plt.xlabel('Time (seonds)')
plt.ylabel('Drag resistance (N)')
plt.title('Drag resistance vs Time')
plt.show()

#Rolling resitance force
# instead of 0 for angle, need (gradient of track) at different points.
roll_res = roll_res_co*car_mass*9.81*np.cos(0)

#Gradient resistance force
grad_res = car_mass*9.81*np.sin(0)  # need gradient (angle) again

#Required tractive force to achieve certain acceleration
# Not sure if this is correct.
acceleration = np.nan_to_num(np.gradient(speed_ms, time_s))
acc_force = car_mass*acceleration  # Force due to acceleration
trac_force = np.array(drag_resis + roll_res + grad_res +
                      acc_force)  # tractive force
# remove negatives from trac_force as no power required from accum to decelerate.
trac_force[trac_force < 0] = 0
####################################################################################################################################
##Power requirement calculations

#Power demand at wheels
power_whe = trac_force*speed_ms  # power requirement at wheels
power_inv = power_whe/motor_eff  # power requirement at inverter
power_acc = (power_inv/inv_eff)/1000  # power requirement at accumulator

#plt.figure(figsize=(120, 4))
#plt.xticks(np.arange(min(time_s), max(time_s)+1, 5))
plt.figure(figsize=(10, 10))
plt.plot(time_s, power_acc)
plt.xlabel('Time (seonds)')
plt.ylabel('Power requirement of accumulator (kW)')
plt.title('Power vs Time')
plt.show()

#######################################################################################################################################
#Capacity requirement of accumulator calculation
energy = trapz(power_acc, time_s)/3600
energy2 = np.ceil(energy*1.3)
print('Required capacity of the accumualtor: '+str(energy) + ' kWh')
print('Required capacity with FOS of 1.3: ' + str(energy2) + ' kWh')
#########################################################################################################################################
