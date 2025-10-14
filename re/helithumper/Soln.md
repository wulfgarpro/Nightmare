# Soln

I solved this RE challenge using Ghidra.

Per, `main`, the user's input is read in via `scanf` and passed to `validate`.

Validate does a char by char comparison of the user's input to a stack string:

```
local_48[0] = 0x66;
local_48[1] = 0x6c;
local_48[2] = 0x61;
local_48[3] = 0x67;
local_48[4] = 0x7b;
local_48[5] = 0x48;
local_48[6] = 0x75;
local_48[7] = 0x43;
local_48[8] = 0x66;
local_48[9] = 0x5f;
local_48[10] = 0x6c;
local_48[0xb] = 0x41;
local_48[0xc] = 0x62;
local_48[0xd] = 0x7d;
```

We can decode the ASCII control codes to determine the correct string.

The easiest way to do that is to munge the hex in vim and throw it at CyberChef:

`0x66 0x6c 0x61 0x67 0x7b 0x48 0x75 0x43 0x66 0x5f 0x6c 0x41 0x62 0x7d`

Becomes:

`flag{HuCf_lAb}`

```sh
❯ ./rev
Welcome to the Salty Spitoon™, How tough are ya?
flag{HuCf_lAb}
Right this way..
```
