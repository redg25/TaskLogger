import csv
import json
import re
from os import path
from datetime import datetime as dt
import sqlite3


LEVELS = ('DEBUG', 'INFO', 'WARNING', 'ERROR','CRITICAL')

class CsvHandler():
    """
    Class to create the log handler on a csv file.
    Create a new csv file.
    If the file already exists, it will be amended with the new log entries
    :param filename: str ending with .csv
    """

    def __init__(self, filename: str):
        p = re.compile(r'^.*\.csv$')
        if p.search(filename) == None:
            raise ValueError (f'File has to be a csv')
        header = ['date', 'level', 'message']
        self.filename = filename
        if not path.exists(filename):
            with open (filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)

    def _append_log(self, *args):
        # Append new log entry to csv handler file
        with open (self.filename, 'a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow(args)

    def get_logs(self):
        """
        Get all log entries for the CsvHandler object.
        :return: List of dictionaries [{'Date':...,'Level':...,'Message':...}]
        """
        # Retrieve csv file log as a list of dictionaries
        # amd convert timestamps value to python datetime type
        dict_log = []
        with open(self.filename, 'r') as file:
            dreader = csv.DictReader(file)
            for i, row in enumerate(dreader):
                dict_log.append({'date': row['date'], 'level': row['level'], 'message': row['message']})
        for dic in dict_log:
            dic['date'] = _convertDateInput(dic['date'], 'CSV log')
        return dict_log


class JsonHandler():
    """
    Class to create the log handler on a json file.
    Create a new json file.
    If the file already exists, it will be amended with the new log entries
    :param filename: str ending with .json
    """

    def __init__(self, filename: str):
        p = re.compile(r'^.*\.json$')
        if p.search(filename) == None:
            raise ValueError (f'File has to be a .json')
        self.filename = filename
        if not path.exists(filename):
            jsonlog = []
            with open(self.filename, 'w') as file:
                json.dump(jsonlog, file)

    def _append_log(self,*args):
        # Parse json entry to handler dictionary format
        # Extract log entries for current json file
        # Append new log entry to json data
        # Rewrite json file with updated data
        jsonEntry = {'date': args[0], 'level':args[1], 'message': args[2]}

        with open (self.filename, 'r') as file:
            jsonlog = json.load(file)
        jsonlog.append(jsonEntry)
        with open(self.filename, 'w') as file:
            json.dump(jsonlog, file, indent=4)

    def get_logs(self):
        """
        Get all log entries for the JsonHandler object.
        :return: List of dictionaries [{'Date':...,'Level':...,'Message':...}]
        """
        # Retrieve json file log as a list of dictionaries
        # amd convert timestamps value to python datetime type
        with open(self.filename, 'r') as file:
            dict_log = json.load(file)
        for dic in dict_log:
            dic['date'] = _convertDateInput(dic['date'], 'CSV log')
        return dict_log


class SqlHandler():
    """
    Class to create the log handler on a sqlite file.
    Create a new sqlite file.
    If the file already exists, the logEntry table is amended with the new log entries
    :param filename: str ending with .sqlite
    """
    sql_create_log_entry_table = """ CREATE TABLE IF NOT EXISTS logEntry (
                                        id integer PRIMARY KEY,
                                        date text NOT NULL,
                                        level text NOT NULL,
                                        message  text NOT NULL
                                    ); """
    def __init__(self, filename: str):
        p = re.compile(r'^.*\.sqlite$')
        if p.search(filename) == None:
            raise ValueError (f'File has to be a sqlite')
        self.filename = filename
        self.conn = sqlite3.connect(self.filename)
        c = self.conn.cursor()
        c.execute(self.sql_create_log_entry_table)
        self.conn.close()

    def _append_log(self, *args):
        # Append new log entry to csv handler file
        sql = ''' INSERT INTO logEntry(date,level,message)
              VALUES(?,?,?) '''
        self.conn = sqlite3.connect(self.filename)
        cur = self.conn.cursor()
        cur.execute(sql, args)
        self.conn.commit()
        self.conn.close()

    def get_logs(self):
        """
        Get all log entries for the CsvHandler object.
        :return: List of dictionaries [{'Date':...,'Level':...,'Message':...}]
        """
        # Retrieve csv file log as a list of dictionaries
        # amd convert timestamps value to python datetime type
        dict_log = []
        sql = ''' SELECT * FROM logEntry '''
        self.conn = sqlite3.connect(self.filename)
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        self.conn.commit()
        self.conn.close()
        for row in rows:
            dict_log.append({'date': row[1], 'level': row[2], 'message': row[3]})
        for dic in dict_log:
            dic['date'] = _convertDateInput(dic['date'], 'CSV log')
        return dict_log


class FileHandler():
    """
    Class to create the log handler on a txt file.
    Create a new txt file.
    If the file already exists, it will be amended with the new log entries
    :param filename: str ending with .txt
    """

    def __init__(self, filename: str):
        p = re.compile(r'^.*\.txt$')
        if p.search(filename) == None:
            raise ValueError (f'File has to be a txt')
        self.filename = filename
        if not path.exists(filename):
            with open (filename, 'w') as file:
                pass

    def _append_log(self, *args):
        # Append new log entry to txt handler file
        entry = (f'{"|".join(args)}\n')
        with open (self.filename, 'a') as file:
            file.write(entry)


    def get_logs(self):
        """
        Get all log entries for the CsvHandler object.
        :return: List of dictionaries [{'Date':...,'Level':...,'Message':...}]
        """
        # Retrieve csv file log as a list of dictionaries
        # amd convert timestamps value to python datetime type
        dict_log = []
        with open(self.filename, 'r') as file:
            entries = file.readlines()
            for row in entries:
                lst_entry = row.split('|')
                dict_log.append({'date': lst_entry[0], 'level': lst_entry[1], 'message': lst_entry[2].replace('\n','')})
        for dic in dict_log:
            dic['date'] = _convertDateInput(dic['date'], 'CSV log')
        return dict_log


class ProfilLogger:
    """
    Class to set the profile of the logger and to log new entries in the handler(s).
    :params handlers: List of handler object instances CsvHandler, JsonHandler...
    """

    def __init__(self, handlers):
        self.handlers = handlers
        self.level = LEVELS[0]

    def debug(self, message: str):
        """
        Log entries in handler with the DEBUG level
        :param message: Text to be logged with the log entry.
        Ex: obj.debug("Connection failed")
        """
        if LEVELS.index(self.level) == 0:
            LogEntry(dt.now().strftime('%Y/%m/%d %H:%M:%S'), LEVELS[0], message, self.handlers)

    def info(self, message: str):
        """
        Log entries in handler with the INFO level
        :param message: Text to be logged with the log entry.
        Ex: obj.debug("Connection failed")
        """
        if LEVELS.index(self.level) <= 1:
            LogEntry(dt.now().strftime('%Y/%m/%d %H:%M:%S'), LEVELS[1], message, self.handlers)

    def warning(self, message: str):
        """
        Log entries in handler with the WARNING level
        :param message: Text to be logged with the log entry.
        Ex: obj.debug("Connection failed")
        """
        if LEVELS.index(self.level) <= 2:
            LogEntry(dt.now().strftime('%Y/%m/%d %H:%M:%S'), LEVELS[2], message,self.handlers)

    def error(self, message: str):
        """
        Log entries in handler with the ERROR level
        :param message: Text to be logged with the log entry.
        Ex: obj.debug("Connection failed")
        """
        if LEVELS.index(self.level) <= 3:
            LogEntry(dt.now().strftime('%Y/%m/%d %H:%M:%S'), LEVELS[3], message, self.handlers)

    def critical(self, message: str):
        """
        Log entries in handler with the CRITICAL level
        :param message: Text to be logged with the log entry.
        Ex: obj.debug("Connection failed")
        """
        LogEntry(dt.now().strftime('%Y/%m/%d %H:%M:%S'), LEVELS[4], message, self.handlers)

    def set_log_level(self,level: str):
        """
        Set minimum log level.
        :param level: List of level in order is 'DEBUG', 'INFO', 'WARNING', 'ERROR','CRITICAL'
        """
        # If level input is not valid, the minimum level will stay as currently assigned
        # in the self.level variable
        if level not in LEVELS:
            print("This is not a valid log level")
        else:
            self.level = level


class LogEntry:
    """
    Class to log an entry in handler(s)
    It can be called manually but usage is to trigger it from the ProfilLogger class
    with one of the level method
    Ex: ProfilLogger.info(message)
    :params args: date as datetime type
                  level as str type
                  message as str
                  instance(s) of handler objects
    """
    def __init__(self, *args):
        if type(args[2])!= str:
            raise ValueError('Provide a string as log message')
        for handler in args[3]:
            handler._append_log(*args[:3])


class ProfilLoggerReader:
    """
    Class to access log entries from different handlers.
    Method to filter results based on specific queries:
        - find_by_text
        - find_by_regex
        - group_by_level
        - group_by_month
    :params: handler: instance of handler object
    """

    def __init__(self, handler):
        self.handler = handler

    def find_by_text(self, message: str, start_date: str = None, end_date: str = None):
        """
        Find logs which contain a specific string
        and optionally in a specific time frame
        :param message: string to search
        :param start_date:
        :param end_date:
        :return: List of dictionnaries with log entries
        """
        dict_log = _format_validate_dates(self.handler,start_date,end_date)
        dict_log = [x for x in dict_log if message in x['message']]
        print(f'Log entries containing {message}')
        for log in dict_log:
            print (log)
        return dict_log

    def find_by_regex(self, regex: str,start_date: str = None, end_date: str = None):
        """
        Find logs which match a specific regex
        and optionally in a specific time frame
        :param regex: regex pattern to match
        :param start_date:
        :param end_date:
        :return: List of dictionnaries with log entries
        """
        dict_log = _format_validate_dates(self.handler,start_date,end_date)
        p = re.compile(regex)
        dict_log = [x for x in dict_log if p.search(x['message'])!=None]
        print (f'Log entries matching {regex}:')
        for log in dict_log:
            print(log)
        return dict_log

    def group_by_level(self,start_date: str = None,end_date: str = None):
        """
        Group logs by level
        and optionally in a specific time frame
        :param start_date:
        :param end_date:
        :return: Dictionnaries with log entries, level as keys
        """
        dict_log = _format_validate_dates(self.handler,start_date,end_date)
        level_dict = {'DEBUG': [], 'INFO': [], 'WARNING': [], 'ERROR': [], 'CRITICAL': []}
        # Loop through log entries to group them by level
        # and create the dictionary
        for key in level_dict.keys():
            for log_entry in dict_log:
                if log_entry['level'] == key:
                    level_dict[key].append(log_entry)
        print (f'Log entries grouped by level')
        for key, value in level_dict.items():
            print(f'{key}:{value}')
        return level_dict

    def group_by_month(self,start_date: str =None, end_date: str =None):
        """
        Group logs by month
        and optionally in a specific time frame
        :param start_date:
        :param end_date:
        :return: Dictionnaries with log entries, month number as keys
        """
        dict_log = _format_validate_dates(self.handler,start_date,end_date)
        month_dict = {}
        # Loop through log entries to group them by month
        # and create the dictionary
        for log_entry in dict_log:
            key = f'{str(log_entry["date"].year)}-{str(log_entry["date"].month)}'
            if key not in month_dict:
                month_dict[key] = [log_entry]
            else:
                month_dict[key].append(log_entry)
        print (f'Log entries grouped by month')
        for key,value in month_dict.items():
            print(f'{dt.strptime(key,"%Y-%m").strftime("%Y-%B")}:{value}')
        return month_dict

def _format_validate_dates(handler: object,start_date: str = None, end_date: str = None,):
    start_date, end_date = _validate_dates(start_date, end_date)
    if start_date and end_date and end_date < start_date:
        raise ValueError(f'End date cannot be before start date')
    else:
        dict_log = handler.get_logs()
        dict_log = _filter_by_date(dict_log, start_date, end_date)
        return dict_log

# Retrieve dates as datetime type
def _validate_dates(start_date: str, end_date: str):
    if start_date:
        start_date = _convertDateInput(start_date, 'start date')
    if end_date:
        end_date = _convertDateInput(end_date, 'end date')
    return start_date, end_date

# Check user input and convert dates to datetime type from str type
def _convertDateInput(date: str,date_type: str):
    try:
        return dt.strptime(date, '%Y/%m/%d %H:%M:%S')
    except Exception as e:
        print(f'Validation error: Date format for {date_type} should be: YYYY/MM/DD HH:MM:SS')
        raise

# Filter entry logs based on user input time frame
def _filter_by_date(dict_log: list, start_date: str, end_date: str):
    if start_date:
        dict_log = [x for x in dict_log if x['date'] > start_date]
    if end_date:
        dict_log = [x for x in dict_log if x['date'] < end_date]
    return dict_log





