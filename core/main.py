#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

# Author: funchan
# CreateDate: 2021-05-12 12:57:40
# Description: 在保证笔记本电脑屏幕处于最佳分辨率的前提下，根据电源模式自动设置屏幕亮度、刷新率，适用于安装了Windows系统的笔记本电脑

import ctypes
import logging
import time
from collections import namedtuple
from ctypes import wintypes

import win32api
import wmi

from dirs import *
from log import log


def get_system_power_status():
    class SYSTEM_POWER_STATUS(ctypes.Structure):
        _fields_ = [('ACLineStatus', wintypes.BYTE),
                    ('BatteryFlag', wintypes.BYTE),
                    ('BatteryLifePercent', wintypes.BYTE),
                    ('SystemStatusFlas', wintypes.BYTE),
                    ('BatteryLifeTime', wintypes.DWORD),
                    ('BatteryFullLifeTime', wintypes.DWORD)]

    SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)
    GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
    GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
    GetSystemPowerStatus.restype = wintypes.BOOL

    system_power_status = SYSTEM_POWER_STATUS()
    system_power_status_p = ctypes.pointer(system_power_status)
    if not GetSystemPowerStatus(system_power_status_p):
        raise ctypes.WinError()

    return system_power_status


def change_display_brightness(brightness):
    if 40 <= brightness <= 100:
        worker = wmi.WMI(namespace='root\WMI').WmiMonitorBrightnessMethods()[0]
        worker.WmiSetBrightness(Brightness=brightness, Timeout=500)


def get_required_devmode():
    Devmode = namedtuple(
        'Devmode', ['index', 'width', 'height', 'pixel', 'bit', 'frequency'])
    devmode_list = []

    i = 0
    while True:
        try:
            ds = win32api.EnumDisplaySettings(None, i)
            devmode_list.append(
                Devmode(i, ds.PelsWidth, ds.PelsHeight,
                        ds.PelsWidth * ds.PelsHeight, ds.BitsPerPel,
                        ds.DisplayFrequency))
        except BaseException:
            break

        i += 1

    max_pixel = max([d.pixel for d in devmode_list])
    max_bit = max([d.bit for d in devmode_list if d.pixel == max_pixel])
    required_devmode_list = [
        d for d in devmode_list if (d.pixel == max_pixel and d.bit == max_bit)
    ]
    required_devmode_list.sort(key=lambda x: x.frequency, reverse=True)

    if len(required_devmode_list) >= 2:
        devmode_performance_index = required_devmode_list[0].index
        devmode_savepower_index = required_devmode_list[-1].index
    else:
        devmode_performance_index = devmode_savepower_index = required_devmode_list[
            0].index

    devmode_performance = win32api.EnumDisplaySettings(
        None, devmode_performance_index)
    devmode_savepower = win32api.EnumDisplaySettings(None,
                                                     devmode_savepower_index)

    return devmode_performance, devmode_savepower


def change_display_mode(devmode):
    win32api.ChangeDisplaySettings(devmode, 0)


def main():
    logger = log(log_dir, log_level=logging.INFO)

    devmode_performance, devmode_savepower = get_required_devmode()

    while True:
        system_power_status = get_system_power_status()
        power_plugged = bool(system_power_status.ACLineStatus)
        power_percent = system_power_status.BatteryLifePercent

        if power_plugged:
            brightness = 100
            devmode = devmode_performance

        else:
            brightness = 50 + int(power_percent * 0.3)
            devmode = devmode_savepower

        change_display_brightness(brightness)
        change_display_mode(devmode)

        logger.info(
            f'外接电源：{power_plugged}, 电池余量：{power_percent}%, 屏幕亮度：{brightness}%, 屏幕刷新率：{devmode.DisplayFrequency}'
        )

        time.sleep(120)


if __name__ == '__main__':
    main()
