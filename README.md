# serials-data-collector
Python script for collecting and storing data about new serials episodes from http://seasonvar.ru.

PostgreSQL 13.4 required. If flag -u or --update will be passed to programm (python3 main.py -u (--update)) programm will try to store collected data into a database SerialsData, so one is required.

Connection to database could be established via CONNECTION_STRING.

Example of table for storing collected data:

CREATE TABLE collected_data (

    serial_id smallint not null check(serial_id >= 0),
    serial_name varchar(128) not null check(length(serial_name) > 0),
    serial_episodes_added varchar(32) not null check(length(serial_episodes_added) > 0),
    serial_link varchar(128) not null check(length(serial_link) > 0),
    serial_imdb_rating numeric(2, 1) check ( serial_imdb_rating > 0),
    serial_voted_for_rating integer check(serial_voted_for_rating > 0),
    serial_date_of_adding date not null
);

![image](https://user-images.githubusercontent.com/86420598/152660770-5927386b-5ba5-4aeb-8a45-1b5f1a2ebcdf.png)
