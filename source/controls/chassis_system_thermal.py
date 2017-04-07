#**************************************************************
#*                                                            *
#*   Copyright (C) Microsoft Corporation. All rights reserved.*
#*                                                            *
#**************************************************************

import dbus
import dbus.service
import collections
import math

from obmc.dbuslib.bindings import get_dbus, DbusProperties, DbusObjectManager
from utils import completion_code

DBUS_NAME = 'org.openbmc.Sensors'
DBUS_INTERFACE = 'org.freedesktop.DBus.Properties'

SENSOR_VALUE_INTERFACE = 'org.openbmc.SensorValue'
SENSOR_THRESHOLD_INTERFACE = 'org.openbmc.SensorThresholds'
SENSOR_HWMON_INTERFACE = 'org.openbmc.HwmonSensor'

bus = get_dbus()

def get_sensor_name(sensor_path):
    path_list = sensor_path.split("/")
    return path_list[-1]

sensor_mainboard_temperature_table =\
[\
    "/org/openbmc/sensors/temperature/TMP1",\
    "/org/openbmc/sensors/temperature/TMP2",\
    "/org/openbmc/sensors/temperature/TMP3",\
    "/org/openbmc/sensors/temperature/TMP4",\
    "/org/openbmc/sensors/temperature/TMP5",\
    "/org/openbmc/sensors/temperature/TMP6",\
    "/org/openbmc/sensors/temperature/TMP7",\
    "/org/openbmc/sensors/temperature/TMP8"
]

sensor_fan_pwm_table =\
[\
    "/org/openbmc/control/fan/fan1",
    "/org/openbmc/control/fan/fan2",
    "/org/openbmc/control/fan/fan3",
    "/org/openbmc/control/fan/fan4",
    "/org/openbmc/control/fan/fan5",
    "/org/openbmc/control/fan/fan6"
]

sensor_fan_rpm_table =\
[\
    "/org/openbmc/sensors/fan/fan_tacho1",
    "/org/openbmc/sensors/fan/fan_tacho2",
    "/org/openbmc/sensors/fan/fan_tacho3",
    "/org/openbmc/sensors/fan/fan_tacho4",
    "/org/openbmc/sensors/fan/fan_tacho5",
    "/org/openbmc/sensors/fan/fan_tacho6",
    "/org/openbmc/sensors/fan/fan_tacho7",
    "/org/openbmc/sensors/fan/fan_tacho8",
    "/org/openbmc/sensors/fan/fan_tacho9",
    "/org/openbmc/sensors/fan/fan_tacho10",
    "/org/openbmc/sensors/fan/fan_tacho11",
    "/org/openbmc/sensors/fan/fan_tacho12"
]

def get_chassis_thermal():
    result = {}
    result['temperatures'] = collections.OrderedDict()
    result['fans'] = collections.OrderedDict()

    try:
        for index in range(0, len(sensor_mainboard_temperature_table)):
            property = {}
            property['sensor_id'] = index+1
            property['sensor_number'] = 0
            property['sensor_name'] = get_sensor_name(sensor_mainboard_temperature_table[index])
            property['value'] = 0
            property['upper_critical_threshold'] = 0

            object = bus.get_object(DBUS_NAME, sensor_mainboard_temperature_table[index])
            interface = dbus.Interface(object, DBUS_INTERFACE)

            scale = interface.Get(SENSOR_HWMON_INTERFACE, 'scale')

            value = interface.Get(SENSOR_VALUE_INTERFACE, 'value')

            property['value'] = value

            property['upper_critical_threshold'] = interface.Get(SENSOR_THRESHOLD_INTERFACE, 'critical_upper')

            property['sensor_number'] = interface.Get(SENSOR_HWMON_INTERFACE, 'sensornumber')

            result['temperatures'][str(index)] = property

        for index in range(0, len(sensor_fan_rpm_table)):
            property = {}
            property['sensor_id'] = index+1
            property['sensor_number'] = 0
            property['upper_critical_threshold'] = 0
            property['value'] = 0
            property['PWM'] = 0

            object = bus.get_object(DBUS_NAME, sensor_fan_pwm_table[index/2])
            interface = dbus.Interface(object, DBUS_INTERFACE)

            property['PWM'] = interface.Get(SENSOR_VALUE_INTERFACE, 'value')

            object = bus.get_object(DBUS_NAME, sensor_fan_rpm_table[index])
            interface = dbus.Interface(object, DBUS_INTERFACE)

            property['value'] = interface.Get(SENSOR_VALUE_INTERFACE, 'value')

            property['upper_critical_threshold'] = interface.Get(SENSOR_THRESHOLD_INTERFACE, 'critical_upper')

            result['fans'][str(index)] = property

    except Exception, e:
        print "!!! DBus error !!!\n"

    return result
