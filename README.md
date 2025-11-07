Usage: python3 modular-tool.py file.json

Essentially the toolset currently integrates 5 different algorithms; vigenere, atbash, eulers, autokey and shift.
The code is picky about the JSON contents, example.json has been used as a base for the different functions.

After the initial decryption, it is possible to chain encryption to another.

Some analysis tools are included such as IoC and frequency analysis. Ciphertext has to be on one line, can include seperator symbols etc., phonetics should handle these in the functions.

Todo (at least):
- IC2
- Option to run other stuff such as nth prime, fibono etc.
- More statistical analysis functions
