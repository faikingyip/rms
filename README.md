# rms
A Restaurant Management System built using Python, with Pyside and a Postgresql database. Connections to the database is asynchronous using SqlAlchemy.


## Introduction
This is an ongoing project, intended to embody the best software development practices for readability, maintainbility and testability.

The project is an ongoing one, so it will start small, with a limited set of features, then gradually extended with new features.


## The features
- Manage dining tables (in progress)
- Manage menus and items (queued)
- Styling (queued)


## Setup
1. Run database_setup.sql to set up the postgresql database user and database. Ensure permissios are granted to the database user.
2. Setup .env file using the .env.example as guide.
3. With the database set up, run the following to set up the database tables and create some users:

```
python src/main.py setup
```

- The first user created will be admin, with access pin as supplied in the .env file.
- The first user created will be user, with access pin as supplied in the ,nv file.


4. Now use the following command to run the program:

```
python src/main.py
```

## Technical notes

### Incorrect setting of constants
There are some constants in the PropertiesPanel that need to be
calculated per shape rather than be a constant.

This way we can clear define the boundaries of the movable
area for the context shape from the properties panel.

MIN_SHAPE_X = MIN_SHAPE_Y = 0
MAX_SHAPE_X = MAX_SHAPE_Y = 200
