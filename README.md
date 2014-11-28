Stats
=====

Small Desktop application written in Python 2.7 to keep track of shooting results.

Windows Build
-------------

To build this application into a standalone windows application you need the Python 2.7 libraries numpy, pandas, matplotlib and py2exe installed. Furthermore the DLLs msvcr90.dll and msvcp90.dll are required. Place them into the client folder. Than run the setup.py via

    python setup.py py2exe

This will compile the programm into a standalone Windows program.
