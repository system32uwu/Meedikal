# Technologies used

- Flask (web server)

## NOTES

### Upgrading sqlite3

Due to certain functionality that's only provided by sqlite3+, the standard sqlite3 library that comes with python needs to be upgraded.

#### In Windows

Go to the [sqlite downloads page](https://www.sqlite.org/download.html), and download the [latest precompiled binary for Windows](https://www.sqlite.org/download.html#win32).

Unzip the file, and copy sqlite3.dll to the "DLLs" folder in your python installation location (ex: C:/Python/DLLs, C:/Users/user/AppData/Local/Programs/Python/DLLs), select "Replace file in destination" when prompted.

### In Linux

Install or update sqlite using your distro package manager.

Available in Arch Linux via pacman: `sudo pacman -S sqlite`

### Creating the database

On first run, or when making changes to database schema, run:

```sh
python util/createDb.py
```
