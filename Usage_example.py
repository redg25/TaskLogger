from loggertask import *

#Create handlers
json_handler = JsonHandler("logs.json")
csv_handler = CsvHandler("sample_test_csv_handler.csv")
sql_handler = SqlHandler("logs.sqlite")
file_handler = FileHandler("logs.txt")

#Set logger profile
logger = ProfilLogger(handlers=[csv_handler, json_handler, sql_handler, file_handler])
logger.set_log_level("WARNING")

#Logs test entries
logger.debug("You reach this debug line of code")
logger.info("FYI, this an info message")
logger.warning("Attention, something doesn't look good")
logger.error("There is definitely something wrong")
logger.critical("Nothing can be done, the application is down")

# Logs are being read from the logs.csv file
log_reader = ProfilLoggerReader(handler=csv_handler)
log_reader.find_by_text("something") # returns list of LogEntry that contains the messages: "Attention, something doesn't look good","There is definitely something wrong"
log_reader.find_by_regex(r'[p]{2,}') # returns list of logEntry that contains: "Nothing can be done, the application is down"
log_reader.group_by_level(start_date='2015/01/01 01:01:01',end_date='2021/01/01 01:01:01')
log_reader.group_by_month(start_date='2015/01/01 01:01:01')

