#!/bin/sh

echo "Inserting Users..."
psql ml < data/insert_users.sql

echo "Inserting Businesses..."
psql ml < data/insert_businesses.sql

echo "Inserting Photos..."
psql ml < data/insert_photos.sql

echo "Inserting Checkins..."
psql ml < data/insert_checkins.sql

echo "Inserting Tips..."
psql ml < data/insert_tips.sql

echo "Inserting Reviews..."
psql ml < data/insert_reviews.sql
