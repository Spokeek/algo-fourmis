 This project is an implementation of the Ant colony optimization algorithm.
 
 This project had as an objective to use it to optimize a route to travel through Grand Britain pubs.
 
 To use it, you need the CSV file containing the data on [kaggle.com](https://www.kaggle.com/getthedata/open-pubs) .
 
 Here are the environement variables available
 
|variable name|is required|default value|description|
|---|---|---|---|
|CSV_FILENAME|no|open_pubs.csv|path to the csv to load on startup|
|GOOGLE_API_TOKEN|yes||API key used ( need to be authorised for geocoding and Javascript )
|NUMBER_NODES|no|150|Number of nodes to use on our graph ( no limitation if less or equal to 0 )
|MAP_CENTER|no|True|Center the camera on the HTML output page.
|USE_MILES_UNIT|no|False|Display the distance in Miles, else it would be in Kilometers

This is only a school project, soooo, don't use this in production ^^.