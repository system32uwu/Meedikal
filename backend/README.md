# NOTES

## Setting things up

Create a virtual environment by your preferred means.

Using [venv](https://docs.python.org/3/tutorial/venv.html):

```sh
python -m venv venv
```

Activate the virtual environment:

### On Windows

```sh
./venv/Scripts/activate
```

### On Linux

```sh
source venv/bin/activate
```

Then install the dependencies:

```sh
pip install -r requirements.txt
```

## Creating the database and adding the first administrative user

The file `util/initialData.sql` contains and INSERT statement with some default values for a default administrative user, you may update those values directly or later from the admin panel (in the frontend).

On first run, or when making changes to database schema, run:

```sh
python util/createDb.py
```

## Incoming data shape notes

### For GET

The `/all`, `/surname1`, `/surname1name1`, `/medicalPersoonel/mpHasSpec` user endpoints accept _extraFilters_, such as _role_.

The data shape should be the following:

```json
{
    "extraFilters":{
        "role" : "medicalPersonnel"
    }
}
```

If providing any other filters:

```json
{
    "name1": "juan",
    "name2": "perez",
    "extraFilters":{
        "role" : "medicalPersonnel"
    }
}
```

The filters that don't go inside of _extraFilters_ are actual table attributes, that's why role is an extraFilter. The same applies for any other applicable filter that's not in the table that's being queried.

### For multivalued attributes, or multiple records at once

Provide the name of the table as the key, an inside of it a list containing all objects that are to be operated with.

```json
{
    "userPhone": [{
        "ci": 1234,
        "phone": "32919319"
    },
    {
        "ci": 1234,
        "phone": "42343244"
    }]
}
```

```json
{
    "mpHasSpec": [{
        "ciMp": 1234,
        "title": "ophthalmology"
    },
    {
        "ciMp": 1234,
        "title": "surgery"
    },
    {
        "ciMp": 1234,
        "idSpec": 3
    }]
}
```

In case an ID is not provided for a relationship, provide the UNIQUE attribute of the other table, see the example above that uses the mpHasSpec table (medicalPersonnel(__ciMp__) < mpHasSpec > (__id__ | __title__) Specialty).

## For PUT and PATCH

```json
{
    "attr": {
        "value": "some old value",
        "newValue": "something new to replace the old value with",
    }
}
```

By default the update method will use the = operator, if LIKE were to be used the shape would be the following:

```json
{
    "attr": {
        "value": "some old value",
        "newValue": "something new to replace the old value with",
        "operator": "LIKE"
    }
}
```

This is also valid:

```json
{
    "ci": 123,
    "name": {"value": "mateo", "newValue": "marcos"}
}
```

## For DELETE

You may provide any filters in the body of the requests, in the same way that you would filter records as shown with the previous methods.
