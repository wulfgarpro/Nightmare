# Soln

The answers to questions 1 and 2 are hardcoded in the program.

The answer to question 3 is also hardcoded, but you cannot change the variable `target` that's
checked through conventional input.

You instead must use the insecure call `gets(input)` to overflow `input[43]` into `target` where
you write `0xdea110c8` to call `print_flag()` and reveal the flag.


