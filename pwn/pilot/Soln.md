# Soln

A very simple challenge.

The stack is not NX (see `checksec`).

The program leaks the start of the stack memory where we can put our shellcode.

The buffer is a static size of 0x20, but it reads 0x40.

So we smash the stack, overwrite the return address and point it back to where our shellcode is
on the stack.
