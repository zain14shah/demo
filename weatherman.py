"""
Weatherman
This module generates yearly reports on weather data collected from  Dec 1996 - May 2011.
Report no. 1 gives the yearly max/min temperature and max/min humidity.
Report no. 2 gives the hottest day of the year and the temperature on that day.
"""

import os
import sys

import argparse


max_temp_ = {}
max_temp_date = {}
min_temp_ = {}
max_humidity= {}
min_humidity= {}

parser = argparse.ArgumentParser(prog = 'weatherman',
								 usage = '%(prog)s [report#] [data_dir]',
								 description = 'Generate weather reports')
parser.add_argument('-d', '--data_dir', type = str, choices = ['./weatherdata/'],
					help = 'Directory containing weather data files', required = True)
parser.add_argument('-r', '--report_number', type = int, choices = [1, 2],
					help = '1 for Annual Max/Min Temperature, 2 for Hottest day of each year',
					required = True)
try:
	args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

"""
Used for printing yearly reports.
User gets 2 options.
1 for yearly max/min temperature and max/min humidity.
2 for hottest day of the year and the temperature on that day.
"""

def print_report(report_number):

	if report_number == 1:
		print('{:18}{:15}{:16}{:17}{}'.format('Year', 'MAX Temp', 'MIN Temp', 'MAX Humidity', 'MIN Humidity'))
		for key in sorted(max_temp_):
			print(f'{key} {max_temp_[key]:15} {min_temp_[key]:15} {max_humidity[key]:15} {min_humidity[key]:15}')

	elif report_number == 	2:
		print('{:18}{:15}{}'.format('Year', 'MAX Temp', 'DATE'))
		for key in sorted(max_temp_):
			print(f'{key} {max_temp_[key]:15} {max_temp_date[key]:15}')

"""
Functions asks for the direcory path to be accessed.
It only accepts one path which is: ./weatherdata/
as this is the one we need to return the desired reports.
"""

def weather_directory(data_dir):
	file_list = os.listdir(data_dir)
	for file_name in file_list:

		with open(data_dir + file_name) as data_file:
			monthly_data = data_file.read().splitlines()[2:-1]
			for daily_data in monthly_data:
				daily_data = daily_data.split(',')
				year = int(daily_data[0].split('-')[0])
				date = daily_data[0]
				try:
					max_temp = int(daily_data[1])
					min_temp = int(daily_data[3])
					max_humid = int(daily_data[7])
					min_humid = int(daily_data[9])
				except ValueError:
					continue
				"""
				The .get() function is used to set a default value to the dictionary.
				This value wil be set for each key and replaced by the correct
				value after comparison.
				-99 is set for max values, 999 for min values and 'DATE' for string values.
				Large values are selected to compensate for each value,
				as these values can't be greater than said defaults.
				"""
				max_temp_[year] = max_temp_.get(year, -99)
				max_temp_date[year] = max_temp_date.get(year,'DATE')
				if max_temp > max_temp_[year]:
					max_temp_[year] = max_temp
					max_temp_date[year] = date

				min_temp_[year] = min_temp_.get(year, 999)
				if min_temp < min_temp_[year]:
					min_temp_[year] = min_temp

				max_humidity[year] = max_humidity.get(year, -99)
				if max_humid > max_humidity[year]:
						max_humidity[year] = max_humid

				min_humidity[year] = min_humidity.get(year, 999)
				if min_humid < min_humidity[year]:
					min_humidity[year] = min_humid


def main():
	weather_directory(args.data_dir)
	print_report(args.report_number)


if __name__ == "__main__":
    main()
