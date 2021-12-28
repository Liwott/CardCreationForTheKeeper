# CardCreationForTheKeeper
Card Creation helper for the game https://github.com/kotc-game/kotc.
It consists in a card referencing system and the python package `ccftk` that uses it to generate cards' cost and text.

## Referencing system
The components' (i.e. caveats, activation conditions and costs, target selections and effects) references are listed in the file `data/componentHistory.md`.
An ability's reference is
```
(activation condition)-(activation cost)-(target selection reference)-(effect 1)-(effect 2)-...
```
A spell card's reference is
```
S/(ability)
```
A creature's reference is
```
C.(offense).(defense)-(caveat)/(ability 1)/(ability 2)/...
```

## ccftk package
First thing to do after importing the package is creating a database object from data files, for example the ones in the `data/` folder
```
import ccftk
dbEN=ccftk.DataBase("data/DataMapEN.json")
```
This database object has a `refBareCard` method that allows to generate the text and cost of a card from its reference, as well as a `refAbility` method that does that for a single ability.

## Future directions
- add documentation
- finish French translation
- replace eval with an arithmetic parser
- convert to command line tool
- make version checker who replaces components with their revisions
- make svg card templates and convert to "bare card" creator
