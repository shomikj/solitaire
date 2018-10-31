# solitaire
Simple Solitaire Command Line Game in Python

Instructions for running my code:
- Using an installed version of Python 3, run python Solitaire.py in Terminal
- Command Instructions will be printed to the terminal

Rules for Card Game
- Standard Solitaire with following modifications for simplicity
- Only Card Rank is considered (no suit or color)

- Move Possibilities
1. View new card in deck
2. Move card from deck to tableau
3. Move cards between tableaus (supports multiple cards)
4. Move card from deck to foundation
5. Move card from tableau to foundation (supports 1 card only)

Object Oriented Design with the following classes
- Card: rank, string for printing, and whether it is visible in current game state
- Card_Stack: abstract class, framework for tableaus, foundations, and deck
- Tableau: where cards can be arranged, strict decreasing order 
- Foundation: where cards stored at top, strict increasing order 
- Deck: leftover cards, can only view 1 card at a time
- Game: initialize card placement, process move command, print game state
