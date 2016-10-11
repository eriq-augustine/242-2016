#!/bin/sh

psql ml < create.sql
ruby parse.rb
./insert.sh
psql ml < optimize.sql
