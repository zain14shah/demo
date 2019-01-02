"""Weatherman
This module generates yearly reports on weather data collected from files taken
from the user provided directory.
Report no. 1 gives the max/min temperature and max/min humidity of each year.
Report no. 2 gives the hottest day of each year and the temperature on that day.
"""

import argparse
from collections import defaultdict
import os
import sys


DEFAULT_MAX = -99
DEFAULT_MIN = 999
DEFAULT_STR = 'DATE'


def main():
    """Checks all arguments, creates objects and calls relevant methods."""

    parser = argparse.ArgumentParser(
        prog='weatherman', usage='%(prog)s [report] [data_dir]',
        description='Generate weather reports'
    )
    parser.add_argument(
        '-d', '--data_dir', type=check_directory,
        help='Directory containing weather data files', required=True
    )

    parser.add_argument(
        '-r', '--report_number', type=int, choices=[1, 2],
        help='1 for Annual Max/Min Temperature, 2 for Hottest day of each year',
        required=True
    )

    args = parser.parse_args()

    weather_year_report = WeatherYearReport(args.data_dir)
    weather_year_report.process_weather_data()
    weather_year_report.print_report(args.report_number)


def int_parse_wrapper(data):
    """
    This converts string to int and captures the exception.

    Arguments:
        data (str): containing digits to convert

    Returns:
        (int): int value of string or None in case exceptions occur

    """
    try:
        return int(data)
    except ValueError:
        return None


def check_weather_data(value, default):
    """Checks if the value = default.

    Args:
        value (int): contains int to be checked.
        default: contains default constant.

    Returns:
        Returns - if True. Otherwise returns value.

    """

    if value == default:
        return '-'
    else:
        return value


def check_directory(data_dir):
    """Checks if 'data_dir' is an existing path and is not empty.

    Args:
        data_dir (path): Contains a path.

    Raises:
        ArgumentTypeError: If `data_dir` is an empty path or does not exist.

    Returns:
        data_dir path if True. Prints msg if False.

    """
    if os.path.isdir(data_dir):
        if os.listdir(data_dir):
            return data_dir
        else:
            msg = f'{data_dir} is an empty directory'
            raise argparse.ArgumentTypeError(msg)
    else:
        msg = f'{data_dir} directory does not exist'
        raise argparse.ArgumentTypeError(msg)


class WeatherYearData:
    """This class is used to compare and set values required for processing the
    module.

    """

    def __init__(self):
        self.max_temp = DEFAULT_MAX
        self.min_temp = DEFAULT_MIN
        self.max_temp_date = DEFAULT_STR
        self.max_humid = DEFAULT_MAX
        self.min_humid = DEFAULT_MIN

    def set_weather_data(self, date, max_temp, min_temp, max_humid, min_humid):
        """Compares and sets values according to the method rules.

        Args:
            date (str): contains date for hottest day.
            max_temp (int): Maximum temperature.
            min_temp (int): Minimum temperature.
            max_humid (int): Maximum humidity.
            min_humid (int): Minimum humidity.

        """
        if max_temp and max_temp > self.max_temp:
            self.max_temp = max_temp
            self.max_temp_date = date
        if min_temp and min_temp < self.min_temp:
            self.min_temp = min_temp
        if max_humid and max_humid > self.max_humid:
            self.max_humid = max_humid
        if min_humid and min_humid < self.min_humid:
            self.min_humid = min_humid


class WeatherYearReport:
    """This class deals with processing data and printing reports.
    """

    def __init__(self, data_dir):
        """Args:
            data_dir (path): path directory to collect data from.

        """

        self.weather_data = defaultdict(lambda: WeatherYearData())
        self.data_dir = data_dir

    def process_weather_data(self):
        """Reads data from path provided, calls method to initialize
        and store data in the weather_data dictionary.

        """

        for file_name in os.listdir(self.data_dir):

            with open(self.data_dir + file_name) as data_file:
                for daily_data in data_file.read().splitlines()[2:-1]:
                    daily_data = daily_data.split(',')
                    year = daily_data[0].split('-')[0]
                    date = daily_data[0]
                    max_temp = int_parse_wrapper(daily_data[1])
                    min_temp = int_parse_wrapper(daily_data[3])
                    max_humid = int_parse_wrapper(daily_data[7])
                    min_humid = int_parse_wrapper(daily_data[9])

                    weather_data = self.weather_data[year]

                    weather_data.set_weather_data(
                        date, max_temp, min_temp, max_humid, min_humid
                    )

    def print_report(self, report_number):
        """Prints yearly weather reports:
        Report no. 1 prints max/min values for each year.
        Report no. 2 prints temperature and date for the hottest day of the year.

        Args:
            report_number (int): Expects 1 or 2, for .

        """

        if report_number == 1:
            print('{:18}{:14}{:16}{:16}{}'.format(
                'Year', 'MAX Temp', 'MIN Temp', 'MAX Humidity', 'MIN Humidity')
            )
            for key, yearly_data in sorted(self.weather_data.items()):
                print(
                    f'{key}'
                    f'{check_weather_data(yearly_data.max_temp, DEFAULT_MAX):15}'
                    f'{check_weather_data(yearly_data.min_temp, DEFAULT_MIN):15}'
                    f'{check_weather_data(yearly_data.max_humid, DEFAULT_MIN):15}'
                    f'{check_weather_data(yearly_data.min_humid, DEFAULT_MIN):15}'
                )
        elif report_number == 2:
            print('{:18}{:15}{}'.format('Year', 'MAX Temp', 'Date'))
            for key, yearly_data in sorted(self.weather_data.items()):
                print(
                    f'{key}'
                    f'{check_weather_data(yearly_data.max_temp, DEFAULT_MAX):15}            '
                    f'{check_weather_data(yearly_data.max_temp_date, DEFAULT_STR):15}'
                )


if __name__ == '__main__':
    # This will only be executed when this module is run directly.
    main()
