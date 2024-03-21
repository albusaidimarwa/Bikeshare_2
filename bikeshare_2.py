import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv','new york city': 'new_york_city.csv','washington': 'washington.csv' }

cities = ['chicago','new york city','washington']
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']

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
    city = user_input("Which city would you like to explore? \nPick one of the following cities: chicago, new york city or washington?",1)

    # get user input for month (all, january, february, ... , june)
    month = user_input("Which month (all, january, ... june)?", 2)
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = user_input("Which day? (all, sunday, ... saturday)", 3)

    print('-'*40)
    return city, month, day


def user_input(input_text,input_code):
    """
    safegaure against invalid user input
    input_text is the input entered by the user
    input_code refers to three required user's input;  1 = city, 2 = month, 3 = day
    read_in stores the user's input
    """
    
    while True:
        read_in = input(input_text)
        try:
            if read_in.lower() in cities and input_code == 1:
                break
            elif read_in.lower() in months and input_code == 2:
                break
            elif read_in.lower() in days and input_code == 3:
                break
            else:
                if input_code == 1 or 2 or 3:
                    print("\nYour input is invalid. Please, try again!")
        except ValueError:
            print("Sorry, your input is invalid")
    return read_in.lower()


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
    #load data from a file
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # get month, day, hour from Start Time
    df['Month'] = df['Start Time'].dt.month
    df['Week_Day'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) 

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Week_Day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month_no = df['Month'].mode()[0]
    print('The most common month is: ', months[common_month_no].title()) 
    
    # display the most common day of week
    common_day = df['Week_Day'].mode()[0]
    print('The most common day is: ', common_day)

    # display the most common start hour
    common_start_hour = df['Hour'].mode()[0]
    print('The most common start hour is: ', common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: ', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is: ', common_end_station)

    # display most frequent combination of start station and end station trip
    grouping = df.groupby(['Start Station','End Station'])
    common_station = grouping.size().sort_values(ascending=False).head(1)
    print('\nThe most frequent combination of start station and end station trip is: \n', common_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: ', total_travel_time)
    
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type Counts: ')
    print(df['User Type'].value_counts())
    

    # Display counts of gender 
    if city != 'washington':
        print('\nGender Counts: ')
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
        print('\nBirth Year Summary: ')
        earliest_year = int(df['Birth Year'].min())
        print('The earliest year is: ',earliest_year)
        most_recent_year = int(df['Birth Year'].max())
        print('The most recent year is: ',most_recent_year)
        most_common_year = int(df['Birth Year'].mode()[0])
        print('The most common year is: ',most_common_year)
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_data(df):
    """display the next 5-lines of raw data requested by the user

    """
    print(df.head())
    n = 0
    while True:
        see_raw_data = input('\nWould you like to see the next five lines of raw data? Enter yes or no.\n')
        if see_raw_data.lower() != 'yes':
            return
        n += 5
        print(df.iloc[n:n+5])
        
        
def main():
    while True:
        city, month, day = get_filters()
        print('\n' + '***** '*10 + '\n' + ' ***  '*10 + '\n' + '  *   '*10 + '\n')
        print('You picked the following:\nCity: ',city.title(), '\nMonth: ',month.title(), '\nDay: ', day.title(), '\n' + '-'*40)
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        #display first 5-lines of raw data requested by the user
        while True:
            see_raw_data = input('\nWould you like to see the first five lines of raw data? Enter yes or no.\n')
            if see_raw_data.lower() != 'yes':
                break
            display_data(df)
            break
           
        
        restart = input('\nWould you like to explore other data? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
	
        print('\n' + '***** '*10 + '\n' + ' ***  '*10 + '\n' + '  *   '*10 + '\n')
    

if __name__ == "__main__":
	main()

