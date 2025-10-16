# Soln

Per `objdump -D loop -M intel | less`, `main` is:

```sh
080483fb <main>:
 80483fb:       8d 4c 24 04             lea    ecx,[esp+0x4]
 80483ff:       83 e4 f0                and    esp,0xfffffff0
 8048402:       ff 71 fc                push   DWORD PTR [ecx-0x4]
 8048405:       55                      push   ebp
 8048406:       89 e5                   mov    ebp,esp
 8048408:       51                      push   ecx
 8048409:       83 ec 14                sub    esp,0x14
 804840c:       c7 45 f4 00 00 00 00    mov    DWORD PTR [ebp-0xc],0x0
 8048413:       eb 17                   jmp    804842c <main+0x31>
 8048415:       83 ec 08                sub    esp,0x8
 8048418:       ff 75 f4                push   DWORD PTR [ebp-0xc]
 804841b:       68 c0 84 04 08          push   0x80484c0
 8048420:       e8 ab fe ff ff          call   80482d0 <printf@plt>
 8048425:       83 c4 10                add    esp,0x10
 8048428:       83 45 f4 01             add    DWORD PTR [ebp-0xc],0x1
 804842c:       83 7d f4 13             cmp    DWORD PTR [ebp-0xc],0x13
 8048430:       7e e3                   jle    8048415 <main+0x1a>
 8048432:       b8 00 00 00 00          mov    eax,0x0
 8048437:       8b 4d fc                mov    ecx,DWORD PTR [ebp-0x4]
 804843a:       c9                      leave
 804843b:       8d 61 fc                lea    esp,[ecx-0x4]
 804843e:       c3                      ret
 804843f:       90                      nop
```

`mov DOWRD PTR [ebp-0xc],0x0` initialises `[ebp-0xc]` to zero.

Then, `jmp 804842c` jumps to `cmp DWORD PTR [ebp-0xc],0x13`, after which `jle 8048415`
jumps back to `sub esp,0x8`.

The `sub esp,0x8` instruction moves the stack pointer `-0x8` (the stack grows down) - likely stack
alignment.

After that `push DWORD PTR [ebp-0xc]` pushes the current `[ebp-0xc]` DWORD to the stack.

Next, `push 0x80484c0` pushes another DWORD argument to the stack for the subsequent
`call printf@plt`.

So `8+4+4=16`, the stack has been aligned at 16-bytes.

We can see what the argument is with: `objdump -s -j ".rodata" ./loop`:

```sh
Contents of section .rodata:
 80484b8 03000000 01000200 25642000           ........%d .
```

So the `printf` will pop the format specifier `%d` and read the current stack value as an DWORD
integer.

Then it will resize the stack (remove the 16 bytes) with `add esp,0x10` (0x10 is 16), increment
`[ebp-0xc]` by 1 with `add DWORD PTR [ebp-0xc]` and, again, perform the earlier comparison.

So, this is a simple loop structure in ASM.

The loop will print the count variable until it reaches `0x13` (19).

```sh
❯ ./loop
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 %
```
