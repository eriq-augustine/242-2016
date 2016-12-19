#!/bin/sh

psql ml < create.sql

# Parse the yelp JSON dataset and convert them to SQL files in the 'data' directory.
ruby parse.rb

# Insert the generated files.
./insert.sh

# Add data not from yelp.
psql ml < groundtruth.sql
psql ml < keywords.sql
psql ml < stops.sql

# Create support tables, remove redundant key columns, and add indexes.
psql ml < optimize.sql
