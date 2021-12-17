import MySQLdb

conn = MySQLdb.connect(user='test',
                       passwd='1234',
                       db='jogoteca',
                       host='127.0.0.1',
                       port=3306)