import mysql.connector
import os


class DB:
    def __init__(self):
        # connect to the database

        username = os.environ.get('user_name')
        password = os.environ.get('user_password')

        if not username or not password:
            raise ValueError("Database username or password not set in environment variables.")


        try:
            self.conn = mysql.connector.connect(
                host='database-olap.c5wkoy0cggj5.us-east-2.rds.amazonaws.com',
                user= username,
                password= password,
                database='ashish'
            )
            self.mycursor = self.conn.cursor()
            print('Connection established')
        except:
            print('Connection error')

    def fetch_city_names(self):
        if not self.mycursor:
            raise ConnectionError("Database connection is not established.")


        city = []
        self.mycursor.execute("""
        SELECT DISTINCT(Destination) FROM ashish.flight
        UNION
        SELECT DISTINCT(Source) FROM ashish.flight
        """)

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])

        return city

    def fetch_all_flights(self,source,destination):
        if not self.mycursor:
            raise ConnectionError("Database connection is not established.")


        self.mycursor.execute("""
        SELECT Airline,Route,Dep_Time,Duration,Price FROM flight
        WHERE Source = '{}' AND Destination = '{}'
        """.format(source,destination))

        data = self.mycursor.fetchall()

        return data

    def fetch_airline_frequency(self):
        if not self.mycursor:
            raise ConnectionError("Database connection is not established.")


        airline = []
        frequency = []

        self.mycursor.execute("""
        SELECT Airline,COUNT(*) FROM flight
        GROUP BY Airline
        """)

        data = self.mycursor.fetchall()

        for item in data:
            airline.append(item[0])
            frequency.append(item[1])

        return airline,frequency

    def busy_airport(self):
        if not self.mycursor:
            raise ConnectionError("Database connection is not established.")


        city = []
        frequency = []

        self.mycursor.execute("""
        SELECT Source,COUNT(*) FROM (SELECT Source FROM flight
							UNION ALL
							SELECT Destination FROM flight) t
        GROUP BY t.Source
        ORDER BY COUNT(*) DESC
        """)

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])
            frequency.append(item[1])

        return city, frequency

    def daily_frequency(self):
        if not self.mycursor:
            raise ConnectionError("Database connection is not established.")


        date = []
        frequency = []

        self.mycursor.execute("""
        SELECT Date_of_Journey,COUNT(*) FROM flight
        GROUP BY Date_of_Journey
        """)

        data = self.mycursor.fetchall()

        for item in data:
            date.append(item[0])
            frequency.append(item[1])

        return date, frequency

    def dep_time_and_price(self):
        if not self.mycursor:
            raise ConnectionError("Database connection is not established.")


        if not self.mycursor:
            raise ConnectionError("Database connection is not established.")

        time = []
        frequency = []
        price = []
        self.mycursor.execute("""
        SELECT dep_time,COUNT(*),Price FROM flight
            GROUP BY dep_time,Price
            ORDER BY COUNT(*) DESC
            LIMIT 20
        """)
        data = self.mycursor.fetchall()

        for items in data:
            time.append(items[0])
            frequency.append(items[1])
            price.append(items[2])

        return time,frequency,price
