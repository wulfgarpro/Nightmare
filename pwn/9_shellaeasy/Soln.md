# Soln

The program leaks the start of the buffer `local_4c[64]` that reads the user's input via
`gets(local_4c);`.

Since `gets` is unbounded, the user can supply more than 64 and smash the stack.

```c
undefined4 main(void)

{
  char local_4c [64];
  int local_c;
  
  setvbuf(_stdout,NULL,2,0x14);
  setvbuf(_stdin,NULL,2,0x14);
  local_c = L'\xcafebabe';
  printf("Yeah I\'ll have a %p with a side of fries thanks\n",local_4c);
  gets(local_4c);
  if (local_c != L'\xdeadbeef') {
                    // WARNING: Subroutine does not return
    exit(0);
  }
  return 0;
}
```

The `local_c` variable is on the stack with value of `0xcafebabe` just after `local_4c`:

```c
undefined4        Stack[-0xc]:4  local_c
undefined         Stack[-0x4c]:1 local_4c
```

Since `0x4c-0xc=0x40`, overwrite the variable `local_c` to `0xdeadbeef` with a buffer of 64 + 4 so
the exit isn't called and instead the return is called.

By bypassing `exit`, we can overwrite the return address to our shellcode, stored at `local_4c`, the
very address the program leaks.
