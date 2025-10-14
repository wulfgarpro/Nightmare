# Soln

`main` is Ghidra is 001008a1 (rename it so it's clear).

It asks for a flag - there's a length check that expects the user input to be `>= 0x21`.

If it is, each char from the user's input is passed to `FUN_001007fa` up to length.

Let's walk an iteration of the loop in main that calls `FUN_001007fa`:

  for (counter = 0; counter < user_input_len; counter += 1) {
    lVar1 = FUN_001007fa((int)user_input[counter]);

Assume `user_input[counter]` for `counter=0` is `f`.

  local_10 = 0
  while ((local_10 != -1 && ((int)char_from_user_input != *(int*)(&DAT_00301020 + local_10 * 4)))) {

Loop while:

- local_10 isn't -1
- (&DAT_00301020 + local_10 *4) is not the char_from_user_input

On the first iteration, local_10 is 0 and so char_from_user_input is compared with (&DAT_00301020 + 0 * 4)
which evaluates to DAT_00301020.

The first character at DAT_00301020 is `w`.

    if ((int)char_from_user_input < *(int *)(&DAT_00301020 + local_10 * 4)) {
      local_10 = local_10 * 2 + 1;
    }
    else if (*(int *)(&DAT_00301020 + local_10 * 4) < (int)char_from_user_input) {
      local_10 = (local_10 + 1) * 2;
    }

If char_from_user_input is < `w`, local_10 becomes 0 * 2 + 1 = 1.

The next iteration then see char_from_user_input being compared to (&DAT_00301020 + 1 * 4) which
is `f` and the loop exits.

local_10 is returned as 1.

Back in main:

    lVar1 = FUN_001007fa((int)user_input[counter]);
    if (lVar1 != *(long *)(&DAT_003014e0 + counter * 8)) {

local_10 is compared with another global variable - in this case the variable contains all the
correct indexes into DAT_00301020 local_10 should be after returning correctly out of `FUN_001007fa`.

So, it's a matter of aligning each correct index from DAT_003014e0 with i * 4 into DAT_00301020 to reveal the correct flag.

e.g.

DAT_00301020 + 1 *4
DAT_00301020 + 9* 4
etc.

Indexes from DAT_003014e0 are:

0x1, 0x9,  0x11, 0x27, 0x2, 0x0, 0x12, 0x3, 0x8, 0x12, 0x9, 0x12, 0x11, 0x1, 0x3, 0x13, 0x4, 0x3,
0x5, 0x15, 0x2e, 0xa, 0x3, 0xa, 0x12, 0x3, 0x1, 0x2e, 0x16, 0x2e, 0xa, 0x12, 0x6

So, correct indexes into DAT_00301020 are:

1*4 = 4   (00301020 + 4 = 00301024) = f
9*4 = 36 (00301020 + 36 = 00301044) = l
0x11*4 = 68 (00301020 + 68 = 00301064) = a
0x27*4 = 156 = (00301020 + 156 = 003010bc) = g
...

I did the rest of the arithmetic with Chat GPT:

flag{we_beleaf_in_your_re_future}

```sh
Enter the flag
>>> flag{we_beleaf_in_your_re_future}
Correct!
```
