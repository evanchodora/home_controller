## Home Controller Web Interface

Web interface designed to couple with several home automation/smart home systems at my house.

### Cast-Web-API
Forked from https://github.com/vervallsweg/cast-web-api. Container deisgned to run an API to determine what's playing and control various Google Cast devices in the house.

### Dishwasher
Simple Flask API to read/write a PickleDB (https://pythonhosted.org/pickleDB/) that reads whether the dishwasher is clean or not. Super helpful!

### Garage Controller
Flask API designed to interface with the Chamberlain MyQ WiFi controlled garage door opener to open/close the door and read the current status of the door as well as the last time that it moved.
Needs an `.ENV` file in the `docker-compose.yml` specified location with the `MYQEMAIL` and `MYQPASSWORD` variables for the MyQ online service.

### Grafana Render
Flask API that, on a specified time interval, renders a grafana plot for electricity usage, gas usage, and water usage to display in the web interface. Uses a separate service based on RTLAMR (https://github.com/bemasher/rtlamr) to use a software-defined radio to read from the utility meters and write to an InfluxDB timeseries database.

### Tuya Controller
Simple Flask API service that interfaces with Python Tuya (https://github.com/clach04/python-tuya) to control Tuya smart devices in the home.

### Weather Service
Flask API that periodically polls the OpenWeatherMap API (openweathermap.org) for a specific Zip code to pull the weather data and store it in a PickleDB database (to maintain below the free tier usage of OpenWeatherMap)
Needs an `.ENV` file in the `docker-compose.yml` specified location with the `APIKEY` from OpenWeatherMaps and `ZIP` code variables for the OpenWeatherMap API online service.

### Web Client
Main Flask web page that interfaces with the various Tuya, Dishwasher, and Garage APIs, as well as displaying the weather information, ultility monitor plots, and views from an IP security camera.
