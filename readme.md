# loggertask

loggertask is a module which allows:
- Handling of logs on 4 different file types:csv, json, sqlite, txt.
- Logs retrieval with predefined queries.

## Author

Regis Corblin  
email: regiscorblin@yahoo.fr  
tel: +48530124835  

## Handler classes

class CsvHandler(filename:str)  
class JsonHandler(filename:str)  
class SqlHandler(filename:str)  
class FileHandler(filename:str)  

Parameter  
	- **filename**: name of the file where the logs are saved

Ex: 
```python
myhandler = CsvHandler('logs.csv')
```

## Logger class

ProfilLogger(handlers: List[Handler])

**Parameter**  
	- **handlers**: List of handlers that will be responsible for saving and reading log entries

Ex:
```python
logger = ProfilLogger([myhandler,anotherhandler])
```

**Methods**
| Method signature | Description |
|--|--|
| **debug**(msg: str) | Logs a message with level `DEBUG` |
| **info**(msg: str) | Logs a message with level `INFO` |
| **warning**(msg: str) | Logs a message with level `WARNING` |
| **error**(msg: str) | Logs a message with level `ERROR` |
| **critical**(msg: str) | Logs a message with level `CRITICAL` |
| **set_log_level**(level: str) | Set minimal log level to be saved |

*Order of criticality as above*

Ex:
```python
logger.set_log_level('INFO')
logger.warning('This is a warning')
```

## Log reader class

ProfilLoggerReader(handler: Handler)`

**Parameter**  
	- **handler**: Handler from which entries will be extracted

**Methods**
| Method signature | Description |
|--|--|
| **find_by_text**(text: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[LogEntry] | Find log entries that contain given text. If any datetime is given, filter logs according to that datetime.
| **find_by_regex**(regex: str, start_date: Optional[str] = None, end_date: Optional[str] = None)  -> List[LogEntry] | Finds logs by a given regexp. If any datetime is given, filter logs according to that datetime. |
| **group_by_level**(start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, List[LogEntry]] | Group logs by level. If any datetime is given, filter logs according to that datetime. |
| **group_by_month**(start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, List[LogEntry]] | Group logs by month. If any datetime is given, filter logs according to that datetime. |

*All dates to be given with the following format:'YYYY/MM/DD HH:MM:SS'*

#USAGE

```python
json_handler = JsonHandler("logs.json")
csv_handler = CsvHandler("logs.csv")
sql_handler = SqlHandler("logs.sqlite")
file_handler = FileHandler("logs.txt")

logger = ProfilLogger(handlers=[json_handler, csv_handler, sql_handler, file_handler])
logger.set_log_level("WARNING")
logger.debug("You reach this debug line of code")
logger.info("FYI, this an info message")
logger.warning("Attention, something doesn't look good")
logger.error("There is definitely something wrong")
logger.critical("Nothing can be done, the application is down")

# The logs are stores in logs.json, logs.csv, logs.sqlite and logs.txt

# Logs are being read from the logs.csv file
log_reader = ProfilLoggerReader(handler=csv_handler)
log_reader.find_by_text("something") # returns list of LogEntry that contains the messages: "Attention, something doesn't look good","There is definitely something wrong"
log_reader.find_by_regex(r'[p]{2,}') # returns list of logEntry that contains: "Nothing can be done, the application is down"
log_reader.group_by_level(start_date='2015/01/01 01:01:01',end_date='2021/01/01 01:01:01') #returns dictionary of LogEntry grouped by level that were logged between the specified time frame.
log_reader.group_by_month(start_date='2015/01/01 01:01:01') #returns dictionary of LogEntry grouped by month that were logged after the specified start date.
```
## Testing

You can use the sample of logs sample_test_csv_handler.csv (available on this repository) to run tests on log reader methods  
The file Usage_example.py runs all methods of logs creation for all types of handlers and all log reader methods for the csv test file.
