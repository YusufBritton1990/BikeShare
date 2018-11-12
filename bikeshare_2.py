import time #use for python's strftime
import pandas as pd #can access series methods (strftime)
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
    city = input('Please enter Chicago, New York City, or Washington to view data from these cities: ').lower()
    while city not in CITY_DATA:
        city = input('Entry invalid. Please input Chicago, New York City, or Washington: ').lower() # good. will persist until input is correct

    month = 'all' #default to all in case none is selected
    day = 'all' #default to all in case none is selected
    option = ['month', 'day', 'none']
    response = input('Would you like to filter by month, day, or no filters? please select \'none\' if you want no filters: ').lower()

    # NOTE: Make if statements for month, day, none, and use else to ask to make a specific request
    while response not in option:
        response = input('Entry invalid. Please request a filter of month, day, or none: ').lower() # good. will exist while loop once correct

    if response == 'month':
        # get user input for month (all, january, february, ... , june)
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = input('Please enter a month between January to June: ').lower()
        while month not in months:
            month = input('Entry invalid. Please enter a month between January to June: ').lower() # good. will exist while loop once correct

    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif response == 'day':
        # get user input for month (all, january, february, ... , june)
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        day = input('Please enter a day from Sunday through Saturday: ').lower()
        while day not in days:
            day = input('Entry invalid. Please enter a day from Sunday through Saturday: ').lower() # good. will exist while loop once correct

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")
    #print(df['day_of_week'])

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1 #adding on so month will pull the correct period

        # filter by month to create the new dataframe
        df = df[df['month'] == month]  #good. This is how you filter with pandas

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time() #amount of seconds passed 01/01/1970 (Unix time)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time']) #good

    # display the most common month
    common_month = df['month']

    print('Most common start month: ' + str(common_month.mode()[0]) + ', with ' + str(common_month.value_counts().iloc[0]) + ' entries')#good, but see if you can use format() for the multiple strings

    # ' + str(common_month.mode()[0]) + '

    # display the most common day of week
    common_day = df['day_of_week']
    print('Most common start day: ' + str(common_day.mode()[0]) + ', with ' + str(common_day.value_counts().iloc[0]) + ' entries')#good, but see if you can use format() for the multiple strings

    # display the most common start hour
    common_hour = df['Start Time'].dt.hour
    # print('Most common start hour: ' + str(common_hour.mode()[0]) + ', with ' + str(common_hour.value_counts()[0]) + ' entries')#good, but see if you can use format() for the multiple strings

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_st = df['Start Station']
    print('Most common start station: ' + common_start_st.mode()[0] + ', with ' + str(common_start_st.value_counts()[0]) + ' entries \n')#good, but see if you can use format() for the multiple strings

    # display most commonly used end station
    common_end_st = df['End Station']
    print('Most common end station: ' + common_end_st.mode()[0] + ', with ' + str(common_end_st.value_counts()[0]) + ' entries\n')#good, but see if you can use format() for the multiple strings

    # display most frequent combination of start station and end station trip

    df['Station Combos'] = df['Start Station'] + " , " + df['End Station']
    count_of_combos = df['Station Combos'].value_counts()
    start_and_end = count_of_combos.keys()[0]
    print('\nMost Frequent Combinations of Start and End Station Trip: ', start_and_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    travel_time = df['Trip Duration']

    travel_time_total = pd.to_timedelta(travel_time.sum(), unit='s')

    travel_time_average = pd.to_timedelta(travel_time.mean(), unit='s')

    # display total travel time
    print('Total travel time for period of time: ' + str(travel_time_total) + ', with ' + str(travel_time.count()) + ' entries\n')#good

    # display mean travel time
    print('Average travel time for period of time: ' + str(travel_time_average) + ', with ' + str(travel_time.count()) + ' entries\n')#good

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print(user_types, '\n') #good

    # Display counts of gender
    # NOTE: Making if statement in case washington is used, since it doesn't have this series
    if 'Gender' in df.columns:
        gender = df["Gender"].value_counts()
        print(gender, '\n') #good

    # Display earliest, most recent, and most common year of birth
    # NOTE: Should make a if statement for this in case washington is used
    if 'Birth Year' in df.columns:
        birth_year = df["Birth Year"]

        print('Earliest user birth year: ' + str(int(birth_year.min())))
        print('Oldest user birth year: ' + str(int(birth_year.max())))
        print('Most common birth year: ' + str(int(birth_year.mode())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df) #good
        station_stats(df) #good
        trip_duration_stats(df) #good
        user_stats(df) #good

        # Displays rows of DataFrame
        display_counter = 5
        display_data = input('Would you like to view the the first 5 results?')
        if display_data.lower() == 'yes':
            print(df.head(display_counter))
            display_more = input('Would you like to see the next 5 rows of data?')
            while display_more.lower() == 'yes':
                display_counter += 5
                print(df.head(display_counter))
                display_more = input('Would you like to see the next 5 rows of data?')


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
