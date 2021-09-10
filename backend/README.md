# Technologies used

- Flask (web server)

## NOTES

### Upgrading sqlite3

Due to certain functionality that's only provided by sqlite3+, the standard sqlite3 library that comes with python needs to be upgraded.

#### In Windows

Go to the [sqlite downloads page](https://www.sqlite.org/download.html), and download the [latest precompiled binary for Windows](https://www.sqlite.org/download.html#win32).

Unzip the file, and copy sqlite3.dll to the "DLLs" folder in your python installation location (ex: C:/Python/DLLs, C:/Users/user/AppData/Local/Programs/Python/DLLs), select "Replace file in destination" when prompted.

#### In Linux

Install or update sqlite using your distro package manager.

Available in Arch Linux via pacman: `sudo pacman -S sqlite`

### Creating the database

On first run, or when making changes to database schema, run:

```sh
python util/createDb.py
```

### Incoming data shape notes

#### For GET

The `/all`, `/surname1`, `/surname1name1`, `/medicalPersoonel/mpHasSpec` accept _extraFilters_, such as _userType_.

The data shape should be the following:

```json
{
    "extraFilters":{
        "userType" : "medicalPersonnel"
    }
}
```

If providing any other filters:

```json
{
    "name1": "juan",
    "name2": "perez",
    "extraFilters":{
        "userType" : "medicalPersonnel"
    }
}
```

The filters that don't go inside of _extraFilters_, are table attributes, that's why userType is an extraFilter. The same applies for any other applicable filter that's not in the table that's being queried.

#### For PUT and PATCH

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

In case the _operator_ field is provided to an attribute, it must be provided to the rest of the attributes explicitly:

```json
{
    "attr": {
        "value": "some old value",
        "newValue": "something new to replace the old value with",
        "operator": "LIKE"
    },
    "otherAttr": {
        "value": "some other old value",
        "newValue": "something else new to replace the old value with",
        "operator": "="
    }
}
```
