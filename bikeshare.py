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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York City or Washington ? ")
    while(city.lower() not in ['chicago', 'new york city','washington']):
        city = input("Enter an availaible city amongth 'Chicago', 'New York City' and 'Washington' : ")

    # get user input for month (all, january, february, ... , june)
    month = input("Enter the month you are targeting or 'all' to proceed with all the months: ")
    while(month.lower() not in ['all', 'january','february','march', 'april', 'may','june']):
        month = input("Enter a valid month amongth 'january','february','march', 'april', 'may','june' or enter 'all' to proceed with all the months : ")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter the day of the week you are targeting or 'all' to proceed with all the days: ")
    while(day.lower() not in ['all', 'monday','tuesday','wednesday','thursday','friday','saturday','sunday']):
        day = input("Enter a valid day amongth 'monday','tuesday','wednesday','thursday','friday','saturday','sunday' or enter 'all' to proceed with all the days : ")

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month

    # extract day from the Start Time column to create a day column
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # use the array of months to get the string litteral of the month
    months = ['january', 'february', 'march', 'april', 'may', 'june']

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]

    # find the most common month (from 1=january to 6=june)
    popular_month = months[df['month'].mode()[0]-1]

    # find the most common day (from monday to sunday)
    popular_day = df['day_of_week'].mode()[0]

    # display the most common month
    print('The most frequent start hour: {} \n'.format(popular_hour))

    # display the most common day of week
    print('The most frequent start month: {} \n'.format(popular_month))

    # display the most common start hour
    print('The most frequent start day: {} \n'.format(popular_day))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()    

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most frequent Start Station: {} \n'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most frequent End Station: {} \n'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['start_end_station'] = df['Start Station'].str.cat(df['End Station'], sep=' => ')
    popular_start_end_station = df['start_end_station'].mode()[0]
    print('The most frequent couple (Start Station => End Station) trip : {} \n'.format(popular_start_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time : ", total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time : ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # handle the fact that washington.csv does not include Gender and Birth Year columns 
    try:
        # display counts of gender
        gender = df['Gender'].value_counts()
        print(gender)

        # display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        
        print("The earliest Birth Year : ", earliest_birth_year)
        print("The most recent Birth Year : ", most_recent_birth_year)
        print("The most common Birth Year : ", most_common_birth_year)
    except:
        print("Sorry no statistics availaible for the columns 'Gender' and 'Birth Year' on this data file ! ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        info = input('\nWould you like to see indivudual raw data ? Enter yes or no.\n')
        count = 0
        while(info.lower() == 'yes'):
            print(df.iloc[count : count+5])
            count += 5
            info = input('\nWould you like to see the next raw data ? Enter yes or no.\n')
                
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thanks for exploring data with Python, Good Bye !")
            break

if __name__ == "__main__":
	main()
