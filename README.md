# Startup-Radar-Map Version 1

AI Powered Python tool that turns a plain list of startup websites into an interactive 2‑D map that shows
how similar the companies are and lets a user explore or export clusters. 

![Alt text](https://github.com/humaspasta/Startup-Radar-Map/blob/main/Screenshot%202025-07-21%20172855.jpg)

Functionalities:
1) Efficent and easy to use/understand UI dashboard with chart of all plotted startups.
2) Startups plotted based on their descriptions which allows for a visualization on how similar certain companies are to each other. 
3) In depth AI generated descriptions for each startup along with name, sector, and funding stage information.
4) Lasso tool for observing clusters of points. Points enclosed in the lasso will appear with detailed information below the chart.
5) Export data enclosed in lasso as a csv.


# How to use it:
1) Clone this repository
2) Input an API key for perplexity sonar into the .env file
3) Input desired startups into startups.csv or inputs a file named startups.csv containing a single column with the link of the startups you want analyzed.
4) Run the main file and when prompted in the terminal, open the link in a browser. This will open the plotly dash UI.
5) Use the lasso tool to analyze any startups by clicking and enclosing the dots on the chart.
6) Export the startups in the lasso tool after enclosing by clicking the export button. 

Coming soon:
1) More data and analytics for each startup
2) More ways of representing data(e.g csv format, startups plotted in terms of funding)
3) Improved UI
