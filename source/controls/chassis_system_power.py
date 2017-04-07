#**************************************************************
#*                                                            *
#*   Copyright (C) Microsoft Corporation. All rights reserved.*
#*                                                            *
#**************************************************************

import dbus
import dbus.service
import collections
import obmc_dbuslib
import math

from obmc.dbuslib.bindings import get_dbus, DbusProperties, DbusObjectManager
from utils import completion_code

bus = get_dbus()

DBUS_NAME = 'org.openbmc.Sensors'
DBUS_INTERFACE = 'org.freedesktop.DBus.Properties'

SENSOR_VALUE_INTERFACE = 'org.openbmc.SensorValue'
SENSOR_THRESHOLD_INTERFACE = 'org.openbmc.SensorThresholds'
SENSOR_HWMON_INTERFACE = 'org.openbmc.HwmonSensor'

MAX_PSU_NUM = 6

def get_sensor_name(sensor_path):
    path_list = sensor_path.split("/")
    return path_list[-1]

sensor_power_control_table =\
[\
    "/org/openbmc/sensors/Fans/Fan_HSC_Power_Out",\
    "/org/openbmc/sensors/Fans/Fan_HSC_Status",\
    "/org/openbmc/sensors/Fans/Fan_HSC_Status_MFR"\
]

sensor_power_voltage_table =\
[\
    "/org/openbmc/sensors/pmbus/pmbus01/Voltage_vin",\
    "/org/openbmc/sensors/pmbus/pmbus01/Voltage_vout",\
    "/org/openbmc/sensors/pmbus/pmbus02/Voltage_vin",\
    "/org/openbmc/sensors/pmbus/pmbus02/Voltage_vout",\
    "/org/openbmc/sensors/pmbus/pmbus03/Voltage_vin",\
    "/org/openbmc/sensors/pmbus/pmbus03/Voltage_vout",\
    "/org/openbmc/sensors/pmbus/pmbus04/Voltage_vin",\
    "/org/openbmc/sensors/pmbus/pmbus04/Voltage_vout",\
    "/org/openbmc/sensors/pmbus/pmbus05/Voltage_vin",\
    "/org/openbmc/sensors/pmbus/pmbus05/Voltage_vout",\
    "/org/openbmc/sensors/pmbus/pmbus06/Voltage_vin",\
    "/org/openbmc/sensors/pmbus/pmbus06/Voltage_vout",\
]

sensor_power_powersupplies_table =\
[\
    "/org/openbmc/sensors/pmbus/pmbus01/Power_pout",\
    "/org/openbmc/sensors/pmbus/pmbus02/Power_pout",\
    "/org/openbmc/sensors/pmbus/pmbus03/Power_pout",\
    "/org/openbmc/sensors/pmbus/pmbus04/Power_pout",\
    "/org/openbmc/sensors/pmbus/pmbus05/Power_pout",\
    "/org/openbmc/sensors/pmbus/pmbus06/Power_pout",\
]

def get_chassis_power():
    result = {}
    result['Voltages'] = collections.OrderedDict()

    try:
        # PowerControl

        result['fan_HSC_Power_sensor_name'] = "Fan HSC Power"
        result['power_consumed_watts'] = 'NA'
        result['HSC_status'] = '0x00'
        result['HSC_status_MFR'] = '0x00'

        #Voltages

        for index in range(0, len(sensor_power_voltage_table)):
            object = bus.get_object(DBUS_NAME, sensor_power_voltage_table[index])
            interface = dbus.Interface(object, DBUS_INTERFACE)
            name = 'PSU'+str((index/2)+1)+'_'+get_sensor_name(sensor_power_voltage_table[index])
            property = {}
            property['sensor_id'] = index+1
            property['sensor_name'] = name
            property['sensor_number'] = interface.Get(SENSOR_HWMON_INTERFACE, 'sensornumber')
            property['reading_value'] = 0
            property['upper_critical_threshold']  = interface.Get(SENSOR_THRESHOLD_INTERFACE, 'critical_upper')
            property['lower_critical_threshold']  = interface.Get(SENSOR_THRESHOLD_INTERFACE, 'critical_lower')
            property['min_reading_range']  = interface.Get(SENSOR_HWMON_INTERFACE, 'min_reading')
            property['max_reading_range']  = interface.Get(SENSOR_HWMON_INTERFACE, 'max_reading')

            value = interface.Get(SENSOR_VALUE_INTERFACE, 'value')

            property['reading_value'] = value

            result['Voltages'][str(index)] = property

        #PowerSupplies

        for index in range(0, MAX_PSU_NUM):
            object = bus.get_object(DBUS_NAME, sensor_power_powersupplies_table[index])
            interface = dbus.Interface(object, DBUS_INTERFACE)

            psu_name = 'psu' + str(index+1)

            result[psu_name + '_power_capacity'] = 'NA'
            result[psu_name + '_power_output_watt'] = interface.Get(SENSOR_VALUE_INTERFACE, 'value')
            result[psu_name + '_model_number'] = 'NA'
            result[psu_name + '_serial_number'] = 'NA'
            result[psu_name + '_manufacturer_name'] = 'NA'
            result[psu_name + '_serial_number'] = 'NA'
            result[psu_name + '_part_number'] = 'NA'

    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)

    result[completion_code.cc_key] = completion_code.success

    return result

