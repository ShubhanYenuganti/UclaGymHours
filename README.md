Extension of my CS35L Bruin Active project that now attempts to visualize UCLA gym occupancies on an hour-to-hour basis.
Currently developed the backend that quickly pulls occupancy data from Ucla Rec with BeautifulSoup, stores into MongoDB server and uses Flask for the API.
Next goal is to develop a React frontend that visualizes occupancy of Bfit and Wooden by each hour and then test locally with pulled data on an hour-to-hour basis.
Then deploy it with AWS lambda that automatically runs backend every hour to dynamically load new occupancy data.
