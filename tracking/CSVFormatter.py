## formatter for logfiles
## used by eyetracking and key/mouse inputs

# imports
import logging
import io
import csv

# class
class CSVFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.output=io.StringIO()
        self.writer=csv.writer(self.output)

    def format(self,record):
        record_info = record.msg.split("|")
        self.writer.writerow([record_info[0],record_info[1],record_info[2],record_info[3]])
        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()