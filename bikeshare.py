import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

DAY_DATA = {'0': 'All',
              '1': 'Monday',
              '2': 'Tuesday',
              '3': 'Wednesday',
              '4': 'Thursday',
              '5': 'Friday',
              '6': 'Saturday',
              '7': 'Sunday'}

MONTH_DATA = {'0': 'All',
              '1': 'January',
              '2': 'February',
              '3': 'March',
              '4': 'April',
              '5': 'May',
              '6': 'June'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        cities = ['chicago', 'new york city', 'washington']
        city_input = input('\nPlease enter a valid City:\n- Chicago\n- New York City\n- Washington\n').lower()
        matching_city = [c for c in cities if city_input in c]
        if not matching_city:
            print('City not valid!\n')
        else:
            city = matching_city[0]
            print('>> Selected City: ', city.capitalize())
            break
    
    # get user input for data filter
    while True:
        data_filters = ['day','month','both']
        data_filter_input = input('\nPlease enter a valid filter:\n - Day\n - Month\n - Both\n').lower()
        matching_data_filter = [d for d in data_filters if data_filter_input in d]
        if not matching_data_filter:
            print('Data filter not valid!\n')
        else:
            data_filter = matching_data_filter[0]
            print('>> Selected Filter: ', data_filter.capitalize())
            break        

    # get user input for month (all, january, february, ... , june)
    while True and data_filter in ['month','both']:
        print(MONTH_DATA)
        month = input('\nPlease enter a valid month number:\n')
        if month not in MONTH_DATA:
            print('Month not valid!\n')
        else:
            break
   
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True and data_filter in ['day','both']:
        print(DAY_DATA)
        day = input('\nPlease enter a valid day number:\n')
        if day not in DAY_DATA:
            print('Day not valid!\n')
        else:             
            break

    # Configure data filters for functions    
    if data_filter == 'day':
        month = '0'
    elif data_filter == 'month':
        day = '0'

    print('-'*40)
    print('<< ', city.capitalize(),' >> << ', MONTH_DATA[month],' >> << ', DAY_DATA[day],' >>')
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Load data file
    df = pd.read_csv(CITY_DATA[city.lower()])
    print(df.head())  # start by viewing the first few rows of the dataset!

    # Convert Start-Time into Datetime data
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Convert End-Time into Datetime data
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Insert Hour-Data Column
    df['hour'] = df['Start Time'].dt.hour

    # Insert Day-Data Column
    df['day'] = df['Start Time'].dt.weekday

    # Insert Month-Data Column
    df['month'] = df['Start Time'].dt.month

    # start by viewing the first few rows of the dataset!
    print(df.head())  

    # Filtering the relevant rows regarding the user inputs
    if month != '0' and day != '0':
        df = df[(df['month'] == int(month)) & (df['day'] == int(day))]
    elif month != '0':
        df = df[(df['month'] == int(month))]
    elif day != '0':
        df = df[(df['day'] == int(day))]
 
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    print(df['month'])
    try:
        most_common_month = df['month'].mode()[0]
        print('>> Most common month: ', most_common_month)
    except KeyError:
        print('\n>> Most common month cannot be calculated!\n')

    # display the most common day of week
    try:
        most_common_day = pd.Series(df['day']).mode()[0]
        print('\n>> Most common day of week: ', most_common_day)
    except KeyError:
        print('\n>> Most common day cannot be calculated!\n')

    # display the most common start hour
    try:
        most_common_hour = pd.Series(df['hour']).mode()[0]
        print('\n>> Most common start hour: ', most_common_hour)
    except KeyError:
        print('\n>> Most common hour cannot be calculated!\n')

    # display time used for frequent times of travel
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = pd.Series(df['Start Station']).mode()[0]
    print('\n>> Most common start station: ', most_start_station)

    # display most commonly used end station
    most_end_station = pd.Series(df['End Station']).mode()[0]
    print('\n>> Most common end station: ', most_end_station)

    # display most frequent combination of start station and end station trip
    #most_start_end_station = df[['Start Station','End Station']].value_counts().idxmax() 
    most_start_end_station = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).head(1)
    print('\n>> Most common start-end-combination: ', most_start_end_station.index[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    try:
        total_travel_time = sum(df['Trip Duration'])
        print('\n>> Total travel time: ', total_travel_time)
    except KeyError:
        print('\n>> Total travel time cannot be calculated!\n')

    # display mean travel time
    try:
        mean_travel_time = total_travel_time / len(df['Trip Duration'])
        print('\n>> Mean travel time: ', mean_travel_time)
    except KeyError:
        print('\n>> Mean travel time cannot be calculated!\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        user_types = df['User Type'].value_counts()
        print('>> Counts of user types:\n', user_types);
    except KeyError:
        print('\n>> Counts of user types cannot be calculated!\n')

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('\n>> Counts of gender:\n', gender);
    except KeyError:
        print('\n>> Counts of gender cannot be calculated!\n')

    # Display earliest, most recent, and most common year of birth
    try:        
        birth_year = df['Birth Year'].value_counts()
        print('\n>> Counts of birth year:\n', birth_year);
    except KeyError:
        print('\n>> Counts of birth year cannot be calculated!\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        # Get configuration set
        city, month, day = get_filters()

        # Load data set with configuration
        df = load_data(city, month, day)

        # Calculate time stats
        time_stats(df)

        # Calculate station stats
        station_stats(df)

        # Calculate trip durations
        trip_duration_stats(df)

        # Calculate user stats
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
