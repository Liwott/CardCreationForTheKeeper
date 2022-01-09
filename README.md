# CardCreationForTheKeeper
Card Creation helper for the game https://github.com/kotc-game/kotc.
It consists in a card referencing system and the python package `ccftk` that uses it to generate cards' cost and text.
This whole repo is licensed under the MIT licence.
The `input` method were partially inspired by the cost calculator tool of the [kotc project](https://github.com/kotc-game/kotc), although no code was directly taken from there.

## Referencing system
The components' (i.e. caveats, activation conditions and costs, target selections and effects) references are listed in the file `data/componentHistory.md`.
An ability's reference is
```
(activation condition)-(activation cost)-(target selection)-(effect 1)-(effect 2)-...
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
For example, characteristics of the (10th edition version of the) "Anubis" card are printed via
```
print(dbEN.refBareCard('C.5.25-6.3/18.1-0-5.2-32.2/0-0-3.1.2-10'))
```
Combination with appropriate decoding packages can be used to generate the card texts for sets, as illustrated in the `example.py` file.

## Future directions
- add documentation
- finish French translation
- replace eval with an arithmetic parser
- convert to command line tool
- make version checker who replaces components with their revisions
- make svg card templates and convert to "bare card" creator
