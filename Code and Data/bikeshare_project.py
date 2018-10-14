import time
import pandas as pd
import numpy as np

# This is a tool to do some exploration on the bikeshare data set.  In this tool the user can provide a city and they can filter the city by a list of months
# or a list of days of the week.  After they explore the data they have the option to see a random selection of raw data from the dataset (50 records).  The data
# used is bike share data from the first 6 months of 2017 in the cities of Chicago, Washington DC and New York City.

#Setting up some initial tables and dictionaries
months_list = ['january', 'february', 'march', 'april', 'may', 'june']
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
days_of_week = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (list) months - name of the months to filter by, if no filter is applied all 6 months will be in the list
        (list) day - name of the days of the week to filter by, if no filter is applied all 7 days of the week will be in the list
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        #Using a while loop and returning whatever is sent into a string and lower casing it automatically.  
        #This will allow them to enter the city in any letter case.
        city = str(input('Please input a city that you would like to view bikeshare data on.  Your choices are Chicago, New York City, Washington.\n')).lower()
        print('You chose the city {}'.format(city))
        #Checking if the city is in one of the keys for the CITY_DATA dictionary.
        if city in [key for key in CITY_DATA.keys()]:
            break
        else:
            print('{} is not a valid city, please try again'.format(city))
            continue

    while True:
        #Now we are giving the user a filtering choice.
        filter_choice = str(input('\nDo you want to filter by days, months, both or not at all.  Please type none for not at all\n')).lower()
        #setting the months and days list to all to start if they decide to filter by something we will reset them
        months = months_list[0:6]
        days = days_of_week[0:7]
        choices = ['days','months','both','none']
        #checking if they are sending us valid choices if not we will have the try again
        if filter_choice not in choices:
            print('\nThe filter choice {} is invalid.  Please try again\n'.format(filter_choice))
            continue
        else:
            break       
    if filter_choice == 'both' or filter_choice == 'months':
        #we will always check the month filter if they select both or months
        while True:
            #Instead of passing a single month i am allowing the user to filter by multiple months requesting that they seperate by a comma.  When my wife tested this
            #she put spaces after each comma, so in order to catch that I am going to replace any spaces.
            month = str(input('\nLets filter by months, please choose any of the following months (january,february,march,april,may,june).\nIf you dont want to filter by month type None.\nIf you want to filter by multiple months please list them out and seperate them by a comma (,)\n')).lower().replace(' ','')
            #creating a list to store months that are not valid months that were given by the user
            non_month_list = []
            if month == 'none':
                print('\nYou have decided to not filter by any month\n')
                break
            #I am going to split them into a list of months
            months= month.split(',')
            #Getting distinct values in case they pass the same value twice
            months = list(set(months))
            for month in months:
                if month not in months_list:
                    non_month_list.append(month)
                    break
            #If all months selected are valid (the length of the list is 0) then I will leave the loop, otherwise i am going to have the user redo their input.
            if len(non_month_list) == 0:
                print('\nYou have chosen the following month(s) {}.\n'.format(', '.join(months)))
                break
            else:
                print('\nYou have chosen the following invalid month(s) {}. Please try again at selecting months.\n'.format(', '.join(non_month_list)))
                continue
    if filter_choice == 'both' or filter_choice == 'days':
        #we will always check the day filter if they select both or days
        while True:
            #Allowing the user to filter by multiple days.  They can also choose weekdays or weekends, if those are selected i will select the days for them.
            day = str(input('\nPlease choose a day of the week {}.\nYou can choose multiple days by seperating by a comma.\nYou can choose just weekdays by typing weekdays.\nYou can choose just weekends by typing weekends.\nIf you change your mind and don\'t want to filter by days type none.\n'.format(', '.join(days_of_week)))).lower().replace(' ','')
            #Multiple if statements in case the user changes their mind and doesn't want to filter, wants weekdays, or wants weekends.
            if day == 'none':
                break
            elif day == 'weekdays':
                days = days_of_week[0:5]
                print('\nYou have chosen weekdays!\n')
                break
            elif day == 'weekends':
                days = days_of_week[5:7]
                print('\nYou have chosen weekends!\nYou party animal!')
                break
            else:
            #Checking if the days selected are valid days.
                non_days_list = []
                days = day.split(',')
            #getting the distinct value from the days in case the user passes the same day twice
                days = list(set(days))
                for day in days:
                    if day not in days_of_week:
                        non_days_list.append(day)
                        break

                if len(non_days_list)==0:
                    print('\nYou have chosen the following day(s) {}.\n'.format(', '.join(days)))
                    break
                else:

                    print('\nYou have chosen an invalid day {}.  Please pick the days again.\n'.format(', '.join(non_days_list)))
                    continue
    #Letting the user know their final choices
    print('\nYour final choices are the city of {}, the following month(s) {}, and the following day(s) {}.\n'.format(city,', '.join(months),', '.join(days)))
    print('-'*40)
    return city, months, days

def load_data(city, months, days):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (list) months - name of the months to filter by or all 6 months in months list for all
        (list) days - name of the days of the week to filter by, or all days_of_week to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = df['Start Time'].apply(pd.to_datetime)

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    # filter by months if applicable
    if len(months) < 6:
        # use the index of the months list to get the corresponding int
        months_index = [months_list.index(month)+1 for month in months]
        # filter by month to create the new dataframe
        df = df.loc[df['month'].isin(months_index)]
    # filter by days of week if applicable
    if len(days) < 7:
        # filter by day of week to create the new dataframe
        day_of_week_index = [days_of_week.index(day) for day in days]
        df = df.loc[df['day_of_week'].isin(day_of_week_index)]
    return df
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    #Getting the number of rides in the max month and then getting the Month and subtracting 1 so it matches my months_list index.  I am using idxmax since argmax is deprecated
    common_month_count = df['month'].value_counts().max()
    common_month = months_list[df['month'].value_counts().idxmax() -1]
    print("\nThe most common month to ride is {} with {} rides.\n".format(common_month.title(),str(common_month_count)))
    # TO DO: display the most common day of week
    common_day_count = df['day_of_week'].value_counts().max()
    common_day = days_of_week[df['day_of_week'].value_counts().idxmax()]
    print("\nThe most common day to ride is {} with {} rides.\n".format(common_day.title(),str(common_day_count)))

    # TO DO: display the most common start hour
    common_hour_count = df['hour'].value_counts().max()
    common_hour = df['hour'].value_counts().idxmax()
    print("\nThe most common hour to ride is {} with {} rides.\n".format(str(common_hour),str(common_hour_count)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\nLets give you some time to look at this data\n')
    time.sleep(5)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    #These first two are very similar to the last function just need the max and the idxmax
    pop_start_station_count = df['Start Station'].value_counts().max()
    pop_start_station = df['Start Station'].value_counts().idxmax()
    print("\nThe most common start station is {} with {} rides.\n".format(str(pop_start_station),str(pop_start_station_count)))
    # TO DO: display most commonly used end station
    pop_end_station_count = df['End Station'].value_counts().max()
    pop_end_station = df['End Station'].value_counts().idxmax()
    print("\nThe most common end station is {} with {} rides.\n".format(str(pop_end_station),str(pop_end_station_count)))
    # TO DO: display most frequent combination of start station and end station trip
    #This one is a little different i needed to use a group by to get the counts for both the Start Station and the end station.
    pop_combo_count = df.groupby('Start Station')['End Station'].value_counts().max()
    pop_combo_start, pop_combo_end = df.groupby('Start Station')['End Station'].value_counts().idxmax()
    print("\nThe most common combination of stations is a start station of {} and an end station of {} with {} rides.\n".format(str(pop_combo_start),str(pop_combo_end),str(pop_combo_count)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\nLets give you some time to look at this data\n')
    time.sleep(5)
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    def convert_seconds(seconds):
      # Function to convert the seconds into multiple variables so I can print it out in an easy to read format
      #   Args:
      #       (int) or (float) seconds: time in seconds
      #   Returns:
      #       (list) readable times: Returns of readable list of times (ie 2 days, 2 hours, 2 minutes, 40 seconds)
        minutes,seconds = divmod(seconds,60)
        hours, minutes = divmod(minutes,60)
        days,hours = divmod(hours,24)
        time_dict = {'days':days,'hours':hours,'minutes':minutes,'seconds':seconds}
        readable_times = []
        for key, value in time_dict.items():
            if value > 0:
                readable_times.append(str(value)+' '+key)
        return readable_times
    #Uses convert_seconds function to return the sum of seconds in a readable time format
    print("\nThe total time travelled is {}.\n".format(', '.join(convert_seconds(df['Trip Duration'].sum()))))

    # TO DO: display mean travel time
    #Uses convert_seconds function to return the sum of seconds in a readable time format
    print("\nThe average time travelled per trip is {}.\n".format(', '.join(convert_seconds(df['Trip Duration'].mean()))))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\nLets give you some time to look at this data\n')
    time.sleep(5)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    #Doing a simple value_counts() on the column to get the counts
    print('\nCounts by user type\n')
    print(df['User Type'].value_counts())
    # TO DO: Display counts of gender
    #Doing a simple value_counts() on the column to get the counts
    print('\nCounts by gender\n')
    try:
        
        print(df['Gender'].value_counts())
    except KeyError:
        print('\nSorry gender data is not available for this data set.\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    #Using a similar convention as I did in the time stats function for the common year
    print('\nBirth Year Data\n')
    #After some testing realized this is not going to work for Washington and will need to catch the exception
    try:
        common_year = df['Birth Year'].value_counts().idxmax()
        common_year_count = df['Birth Year'].value_counts().max()
        print("\nThe most common year of birth for a rider is {} with {} riders.\n".format(str(int(common_year)),str(common_year_count)))

        #Recent Year and Earliest Year, converting to integer since it doesn't make sense to have a .0
        recent_year = int(df['Birth Year'].max())
        early_year = int(df['Birth Year'].min())
        print("\nThe most recent year a rider was born in was {}.  The earliest year a rider was born in was {}.\n".format(str(recent_year),str(early_year)))
    except KeyError:
        print('\nSorry Birth year data is not available for this dataset.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\nLets give you some time to look at this data\n')
    time.sleep(5)
def main():
    while True:
        city, months, days = get_filters()
        df = load_data(city, months, days)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        ##Allowing the user to look at a random assortment from the dataframe
        while True:
            raw_data = input('\nWould you like to see some of the raw data\n')
            if raw_data.lower() != 'yes':
                break
            else:
                min_int = np.random.random_integers(len(df)-50)
                max_int = min_int+50
                print(df.iloc[min_int:max_int])
                continue
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
