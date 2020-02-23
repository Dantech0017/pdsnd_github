import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello there! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please input the letter option of the city you are interested in learning more about ("a" for chicago,"b" for new york city, or "c" for washington):\n ').lower()

#while loop checks for letter input or city name input by user. The reason for providing three options (a, b, or c) is to simplify the experience for the user and also prevent any user input errors.
    while True:
        if city == 'a' or city == 'chicago':
            print ("You have selected Chicago, great choice!\n")
            city = 'chicago'
            break
        if city == 'b' or city == 'new york':
            print ("You have selected New York City, great choice!\n")
            city = 'new york city'
            break
        if city == 'c' or city == 'washington':
            print ("You have selected Washington, great choice!\n")
            city = 'washington'
            break
        else:
            print('City input not valid. Let\'s try again! Make sure you to input one of the letter options (a, b, or c), or input the city\'s name.')
            city = input('Please input the letter option of the city you are interested in learning more about ("a" for chicago,"b" for new york city, or "c" for washington): ').lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month_options = {1:'january', 2:'february', 3:'march', 4:'april', 5:'may', 6:'june', 0:'all months'}

    month = int(input("\nNow, please select a month from these options by inputting the number associated with it: {}:\n ".format(month_options)))
    month_numbers = month_options.keys()

    # allows user to try again if input is not within the month options
    while month not in month_numbers:
        month = int(input('\nWe did not recognize that input. \nLet\'s try again! Input the option number here: \n'))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_options = {0:'monday', 1:'tuesday', 2:'wednesday', 3:'thursday', 4:'friday', 5:'saturday', 6:'sunday', 7:'all days of the week'}

    day = int(input("\nLastly, let's select the day of the week. Please select the option number from these options: {}:\n ".format(day_options)))
    day_numbers = day_options.keys()

    # allows user to try again if input is not within the day options
    while day not in day_numbers:
        day = int(input('We did not recognize that input. \nLet\'s try again! Input the option number here: '))

    #while day.lower() not in
    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city])

    # adding columns to verify month and day with start date
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['day'] = pd.to_datetime(df['Start Time']).dt.dayofweek

    # filters the data by month, where 0 = 'all months'
    if month != 0:
        df = df[df['month'] == month]

    # filters the data by day, where 7 = 'all days'
    if day != 7:
        df = df[df['day'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour

    # mode pandas resource: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.mode.html?highlight=mode#pandas.DataFrame.mode
    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]

    # TO DO: display the most common day of week
    most_common_day = df['day'].mode()[0]

    # TO DO: display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    #print(df['day'].mode())
    print("most common month: {} \nmost common day: {} \nmost common hour: {}".format(most_common_month, most_common_day, most_common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    most_common_end = df['End Station'].mode()[0]

    # TO DO: display most frequent combination of start station and end station trip
    df['trips'] = df['Start Station'] + "--" +  df['End Station']
    most_common_trips = df['trips'].mode()[0]
    print("most common start station is: {} \nmost common end station is: {} \nmost common end-to-end stations: {}".format(most_common_start, most_common_end, most_common_trips))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Converting seconds to hour to better display output 
    seconds_in_an_hour = 3600

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_days = total_travel_time//24//seconds_in_an_hour
    total_weeks = total_days // 7
    remainder_days = total_days % 7

    # helpful resource to convert time to seconds: https://www.pythonprogramming.in/convert-time-unit-seconds-in-days-hours-minutes.html

    print("The total travel time is: {} weeks and {} days".format(total_weeks, remainder_days))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_minutes = mean_travel_time // 60
    mean_seconds = mean_travel_time % 60
    print("The mean travel time is: {} minutes and {} seconds".format(mean_minutes, mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # value_counts pandas resource: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.value_counts.html
    print("User Type Counts is: \n{}\n".format(df['User Type'].value_counts()))

    # TO DO: Display counts of gender
    #Washington csv has no gender column
    if city == 'washington':
        print("\nThere is no gender count or birth year available for Washington at this time.\n")
    else:
        print("\nUser gender count is as follows: \n{}\n".format(df['Gender'].value_counts()))
    # TO DO: Display earliest, most recent, and most common year of birth
        earliest_dob = str(int(df['Birth Year'].min()))
        recent_dob = str(int(df['Birth Year'].max()))
        most_common_dob = str(int(df['Birth Year'].mode()))

        print("\nThe earliest birth year is: {}\nThe most recent birth year is: {}\nThe most common birth year is: {}\n".format(earliest_dob, recent_dob, most_common_dob))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city) # Washington csv does not include birth date or gender count columns

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
