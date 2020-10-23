# Auction 3.0 (PyGObject)

Auction 3.0 is a small application to manage a 'Fantaleague' auction.
When the auction is ended it is possible to export the result in a csv file.
Libraries:
* PyGObject 3.34.0:
* pycairo: 1.18.2:
* SQLAlchemy: 1.13.19

## Getting started

Install the packages required in requirements.txt
Launch the main.py file that will create the database:

```
> python main.py
```

### Import Players

From **Player** menu, choose **import** and import MCCnn.txt file.
MCC files are available on [bancaldo's blog](www.bancaldo.wordpress.com) and they are Gazzetta compliant.

### Create Teams

Before starting auction, create at least 2 teams from **Team** menu, choosing **New**.
As default, a new Team is created with standard values imported from 
```
settings.py
```
You can change the default options modifying settings.py file.

### Auction

From **Auction** menu choose **New**.
Filter the player by 'Real Team' name and 'role', then insert the auction value and the Buyer Team which wins the player auction.

### Changes

From **Player** menu it is possible to edit Player data.
From **Team** menu it is possible to edit Team data.

### Trades

When the auction is ended it is possible to exchange players between teams.
Choose **Trades** from **Team** menu.
It's even possible to add extra money during an exchange.

### Export

Finally, when all the auctions end, it's possible to export all data on a csv
file, convenient for importing it into excel.

## Licence

GPL
