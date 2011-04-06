#!/usr/bin/env python

import datetime
import unittest

from csvkit import sql
from csvkit import typeinference

from sqlalchemy import Column
from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String, Time

class TestSQL(unittest.TestCase):
    def test_make_column_name(self):
        c = sql.make_column('test', int, [1, -87, 418000000, None])
        self.assertEqual(c.key, 'test')

    def test_make_column_bool(self):
        c = sql.make_column('test', bool, [True, True, False, None])
        self.assertEqual(type(c.type), Boolean)

    def test_make_column_int(self):
        c = sql.make_column('test', int, [1, -87, 418000000, None])
        self.assertEqual(c.key, 'test')
        self.assertEqual(type(c.type), Integer)

    def test_make_column_float(self):
        c = sql.make_column('test', float, [1.01, -87.34, 418000000.0, None])
        self.assertEqual(type(c.type), Float)

    def test_make_column_datetime(self):
        c = sql.make_column('test', datetime.datetime, [datetime.datetime(2010, 04, 05, 20, 42, 0), datetime.datetime(1910, 04, 05, 20, 37, 21), None])
        self.assertEqual(type(c.type), DateTime)

    def test_make_column_date(self):
        c = sql.make_column('test', datetime.date, [datetime.date(2010, 04, 05), datetime.datetime(1910, 04, 05), None])
        self.assertEqual(type(c.type), Date)

    def test_make_column_time(self):
        c = sql.make_column('test', datetime.time, [datetime.time(20, 42, 0), datetime.time(20, 37, 21), None])
        self.assertEqual(type(c.type), Time)

    def test_make_column_null(self):
        c = sql.make_column('test', str, [None, None, None])
        self.assertEqual(type(c.type), String)

    def test_make_column_string(self):
        c = sql.make_column('test', str, ['this', 'is', 'test', 'data'])
        self.assertEqual(type(c.type), String)

    def test_make_column_string_length(self):
        c = sql.make_column('test', str, ['this', 'is', 'test', 'data', 'that', 'is', 'awesome'])
        self.assertEqual(c.type.length, 7)
    
    def test_column_nullable(self):
        c = sql.make_column('test', int, [1, -87, 418000000, None])
        self.assertEqual(c.key, 'test')
        self.assertEqual(type(c.type), Integer)
        self.assertEqual(c.nullable, True)

    def test_column_not_nullable(self):
        c = sql.make_column('test', int, [1, -87, 418000000])
        self.assertEqual(c.key, 'test')
        self.assertEqual(type(c.type), Integer)
        self.assertEqual(c.nullable, False)

    def test_make_create_table_statement(self):
        statement = sql.make_create_table_statement(
            ['text', 'integer', 'datetime', 'empty_column'],
            [str, int, datetime.datetime, None],
            [
                ['Chicago Reader', 'Chicago Sun-Times', 'Chicago Tribune', 'Row with blanks'],
                [40, 63, 164, None],
                [datetime.datetime(1971, 1, 1, 4, 14), datetime.datetime(1948, 1, 1, 14, 57, 13), datetime.datetime(1920, 1, 1, 0, 0), None],
                [None, None, None, None]
            ])

        self.assertEqual(str(statement).strip(), 
"""CREATE TABLE csvsql (
\ttext VARCHAR(17) NOT NULL, 
\tinteger INTEGER, 
\tdatetime DATETIME, 
\tempty_column VARCHAR(32)
)""")



