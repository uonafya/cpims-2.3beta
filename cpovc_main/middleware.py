"""Print out sql for debugging and sql tuning."""
import os
from django.db import connection
from django.conf import settings


def terminal_width():
    """Function to compute the terminal width."""
    width = 0
    try:
        import struct
        import fcntl
        import termios
        s = struct.pack('HHHH', 0, 0, 0, 0)
        x = fcntl.ioctl(1, termios.TIOCGWINSZ, s)
        width = struct.unpack('HHHH', x)[1]
    except:
        pass
    if width <= 0:
        try:
            width = int(os.environ['COLUMNS'])
        except:
            pass
    if width <= 0:
        width = 80
    return width


class SqlPrintingMiddleware(object):
    """
    Middleware which prints out a list of all SQL queries done.

    for each view that is processed useful for debugging.
    """

    def process_response(self, request, response):
        """Calculate and print the sql durations."""
        indent = 2
        if len(connection.queries) > 0 and settings.DEBUG:
            width = terminal_width()
            total_time = 0.0
            for query in connection.queries:
                nice_sql = query['sql'].replace('"', '').replace(',', ', ')
                sql = "[%s] %s" % (query['time'], nice_sql)
                total_time = total_time + float(query['time'])
                while len(sql) > width - indent:
                    print "%s%s" % (" " * indent, sql[:width - indent])
                    sql = sql[width - indent:]
                print "%s%s\n" % (" " * indent, sql)
            replace_tuple = (" " * indent, str(total_time))
            print "%s[TOTAL PAGE LOAD TIME: %s seconds]" % replace_tuple
        return response
