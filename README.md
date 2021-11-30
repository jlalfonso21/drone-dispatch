# Drone Dispatch

Useful drone functions through API REST for the delivery of small items that are (urgently) 
needed in locations with difficult access.

## Instructions

Guide step-by-step for installing, testing and running the project

### Install

#### Enviroment setup
- You must have Python 3 installed on your system. ([Windows][1], 
[Linux][4], [Mac][2]
or [other OS][3]).
- Ensure this installation have pip inside (`pip --version`), otherwise you must install it manually.
- Open a terminal and change the directory to the current folder that contains the `manage.py` file.
- Run the following command `pip install -r requirements.txt`. This will install all the dependencies of the project.

#### Project setup
- Placed in the project folder from the previous steps, run this command `python manage.py migrate`. This will create
 and run the migrations needed for the local database. 
 (If any error with the previous command, check if python is installed correctly
or try using the version in the command, i.e. `python3 manage.py migrate`).
- To start the daemon for the periodic tasks run in another terminal `python manage.py process_tasks` 
or if your system allows POSIX commands run this in the same terminal `nohup python manage.py process_tasks &`. 
This last one will make the process run (ignoring the HUP signal) in the background without printing to _**STDOUT**_
- To load the testing data run this commands 

```shell script
python manage.py loaddata users.json
python manage.py loaddata meds.json
python manage.py loaddata drones.json
```
- That will install the dummy objects needed for the test. 

### Running the service
- Now we proceed to run the service with `python manage.py runserver`. 
This will run the service in the http://127.0.0.1:8000/ by default, but you can change that by
running `python manage.py runserver server_ip:port` 
where `server_ip` and `port` are your custom values.
- If the backgournd service was stopped, run again `python manage.py process_tasks` to wake the daemon.

### Logging
The file `drones.log` contains the logs that the daemon writes each 10 seconds. Each line have the
following structure:

`Date Time - LogName - LogLevel - Drone - BatteryLevel`

### Testing

- The project include some tests using thedjango testing suite. To run this use `python manage.py test`.
 This will the amount of test and if any test failed (`FAILED failures=n`) or all tests passed (`OK`).

### API REST

The endpoints to use the basic functions of the service are show below,
 replace the content of the `{serial_number}` with the actual value:

|Method |Endpoint|Description|
--- | --- | ---
|POST| `/api/drones/`                             |CREATE OR REGISTER A NEW DRONE|
|GET | `/api/drones/meds/{serial_number}/`        |GET LOADED MEDS FOR A GIVEN DRONE|
|GET | `/api/drones/battery/{serial_number}/`     |GET BATTERY LEVEL OF A GIVEN DRONE|
|POST| `/api/drones/load/{serial_number}/`        |LOAD A GIVEN DRONE WITH MEDICATIONS|
|POST| `/api/drones/clean/{serial_number}/`       |CLEAR CURRENT CARGO OF A GIVEN DRONE|
|GET | `/api/drones/audit/{serial_number}/`       |GET AUDIT LOGS OF A GIVEN DRONE|
|GET | `/api/drones/available/`                   |GET DRONES AVAILABLE FOR LOADING|
|GET | `/api/medication/`                         |GET THE LIST OF MEDICATIONS|
 
### Basic flow (demos)
Basic flow of the service with some demos to try yourself. All the returned contents are `application/json`. 
Change the values as you will, also remember to cange the url if you dont leave the default one.

#### Create new drone
```shell script
curl --location --request POST 'http://127.0.0.1:8000/api/drones/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "serial_number": "SERIAL_NUMBER_01",
    "model": "middleweight",
    "weight_limit": 400.50,
    "battery_capacity": 99
}'
```

#### Get list of medications
```shell script
curl --location --request GET 'http://127.0.0.1:8000/api/medication/'
```

#### Get drone loaded medications
```shell script
curl --location --request GET 'http://127.0.0.1:8000/api/drones/meds/SERIAL_NUMBER_01' \
--header 'Content-Type: application/json'
```

#### Get drone battery level
```shell script
curl --location --request GET 'http://127.0.0.1:8000/api/drones/battery/SERIAL_NUMBER_01' \
--header 'Content-Type: application/json'
```

#### Load a drone with meds
```shell script
curl --location --request POST 'http://127.0.0.1:8000/api/drones/load/SERIAL_NUMBER_01/' \
--header 'Content-Type: application/json' \
--data-raw '[
    {
        "code": "DIP_500_MG",
        "qty": 1
    },
    {
        "code": "DIP_300_MG",
        "qty": 2
    }
]'
```

#### Clean drone cargo
```shell script
curl --location --request POST 'http://127.0.0.1:8000/api/drones/clean/asd/' \
--header 'Content-Type: application/json'
```

#### Get drone audit logs
```shell script
curl --location --request GET 'http://127.0.0.1:8000/api/drones/audit/SERIAL_NUMBER_01'
```

#### Get available drones
```shell script
curl --location --request GET 'http://127.0.0.1:8000/api/drones/available'
```


[1]: https://www.python.org/downloads/windows/

[2]: https://www.python.org/downloads/macos/

[3]: https://www.python.org/download/other/

[4]: https://www.python.org/downloads/source/