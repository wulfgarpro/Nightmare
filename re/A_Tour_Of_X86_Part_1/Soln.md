# Soln.md

**Question 1 : What is the value of dh after line 129 executes? (Answer with a one-byte hex value, prefixed with '0x')**

Line 129 is `xor dh, dh`, this zeroes out `dh` and the answer is: `0x0`.

**Question 2 : What is the value of gs after line 145 executes? (Answer with a one-byte hex value, prefixed with '0x')**

Line 145 is `mov gs, dx`, and since `dx` is zero (per the previous test `cmp dx, 0`), `gs` is: `0x0`.

**Question 3 : What is the value of si after line 151 executes? (Answer with a two-byte hex value, prefixed with '0x')**

Line 151 is `mov si, sp`, and since on line 149 we executed `mov sp, cx` with `cx=0`, `si` is: `si=sp=0`, i.e. `0x0`.

**Question 4 : What is the value of ax after line 169 executes? (Answer with a two-byte hex value, prefixed with '0x')**

**Question 5 : What is the value of ax after line 199 executes for the first time? (Answer with a two-byte hex value, prefixed with '0x')**
