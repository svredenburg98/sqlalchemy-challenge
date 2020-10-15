# sqlalchemy-challenge

In this challenge, I used a combination of sqlalchemy and flask to analyze, visualize and display data related to the weather in Hawaii. 
I first explored the data using a jupyter notebook and sqlalchemy. I queried the database for the rainfall data for the last 12 months, and added it to a pandas dataframe. I then plotted that information using the pandas plot functions and used the '.describe' function to create a summary statistics table. I then ran a query to determine the most active weather station, by grouping by the station and counting the rows for each. This happened to be station USC00519281. I then queried for the temperature data for that most active station and created a histogram of that data. 
Next, I created a flask api application to display some of the queries. It included a page for all the precipitation data, the list of stations, the temperature data for station USC00519281, and a url allowing the user to choose a start and end date and access a page showing the max, min and average temperature for that date range, all in json format.
