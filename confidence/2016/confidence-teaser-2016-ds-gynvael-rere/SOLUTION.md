Solution
========

The main protection in ReRe is the bytecode obfuscation which is achieved in
two ways:

* In each function the bytecode is XORed with a key; when the function execution starts a stub at the end of the bytecode deXORs the main area of the code (yes, this is SMC in Python), jumps there, executes until return (all returns are hooked on "compilation" time), and then reXORs it before returning. This is done separatelly for each and every function in the crackme.
* A lame JUMP_FORWARD + trash bytes are injected into the bytecode; this break dis.dis even after one decrypts the bytecode.

From Python''s perspective, each function from the source code is converted into a function+code constructor calls. Additionally, all strings are encrypted in source, and are decrypted just before the constructors are called; the encryption is placed in a function called _().

The top-level obfuscation has two steps. In the first step, all the functions from crackme.py are obfuscated and thus converted into function+code consturctor calls; these are then put into one huge function called crackme(). In step two, the crackme() function itself undergoes the same obfuscation.

Additionally, the crackme is quite interactive, which produces a lot of noise for any kind of side-channel cracking attempts.


To solve the crackme one should start by figuring out how the _() function is obfuscated, since it has all the strings unencrypted, so it''s easier to hack at it. The goal here is to understand how exactly the obfuscator worked and how to undo it.

Next step is to write a deobfuscator, which should remove both the JUMP_FORWARD parts (either NOP them out, or remove them and relocate the code), deXOR the rest of the bytecode and remove the runtime deciphering code. A bonus is also removing the RETURN_VALUE hooks (which is rather simple to do, as it''s just a jump to a specific piece of code). After this, a Python decompiler should be able to decompile the code.

After this step, one can both decipher all the strings, and deobfuscate first the initial crackme() function, and then all the other functions which crackme() hosts.

The last part is figuring out how the input is checked - this is rather easy going from a function called MaybeGetChar(), which is called only in main() - there one can spot that the returned character is added to a global named INPUT, but only if len(INPUT) is below 26.

Next comes the tracing of where INPUT is used. Just by looking at the co_globals of each function one can spot at least FinalizeFrameBuffer, PrepareFBForBlit, LoadFont and ResetConsole. After digging into them one will have the majority of the flag - enough to guess the rest. If for some reason one is not able to guess "DrgnS{" part, a continued analysis should bring one to the CheckPaletteSync function which does this check.

And that''s it.


