let instance = null;
let wasm_stdout = "";
let memoryStates = new WeakMap();

/**
 * ref: https://stackoverflow.com/a/901144/87207
 */
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function syscall(instance, n, args) {
    switch (n) {
    default:
        console.log("Syscall " + n + " NYI.");
        break;
    case /* brk */ 45: return 0;
    case /* writev */ 146:
        return instance.exports.writev_c(args[0], args[1], args[2]);
    case /* mmap2 */ 192:
        //debugger;
        const memory = instance.exports.memory;
        let memoryState = memoryStates.get(instance);
        const requested = args[1];
        if (!memoryState) {
            memoryState = {
                object: memory,
                currentPosition: memory.buffer.byteLength,
            };
          console.debug(memory.buffer.byteLength);
            memoryStates.set(instance, memoryState);
        }
        let cur = memoryState.currentPosition;
        if (cur + requested > memory.buffer.byteLength) {
            const need = Math.ceil((cur + requested - memory.buffer.byteLength) / 65536);
            memory.grow(need);
        }
        memoryState.currentPosition += requested;
        return cur;
    }
}

/**
 * allocate a region of the given size within the given WebAssembly instance.
 */
function wasm_alloc(instance, size) {
    return syscall(instance, /* mmap */ 192, [0, size]);
}

/**
 * write the given data at the given address within the WebAssembly instance.
 */
function wasm_write(instance, address, buf) {
    const membuf = new Uint8Array(instance.exports.memory.buffer, address);

    for (var i = 0; i < buf.byteLength; i++) {
        membuf[i] = buf[i];
    }
    return null;
}

/**
 * read the given number of bytes from the given address within the given WebAssembly instance.
 */
function wasm_read(instance, address, size) {
    const membuf = new Uint8Array(instance.exports.memory.buffer);
    return membuf.slice(address, address + size);
}

fetch("test.wasm").then(response =>
  response.arrayBuffer()
).then(bytes =>
  WebAssembly.instantiate(bytes, {
    env: {
      /*
       * WASMCEPTION libc.a relies on the symbols for FPU,
       * but we don't really need them...
       **/
      __eqtf2: function() {},
      __multf3: function() {},
      __unordtf2: function() {},
      __addtf3: function() {},
      __eqtf2: function() {},
      __multf3: function() {},
      __subtf3: function() {},
      __netf2: function() {},
      __fixunstfsi: function() {},
      __floatunsitf: function() {},
      __fixtfsi: function() {},
      __floatsitf: function() {},
      __extenddftf2: function() {},

      /* trampoline to our js syscall handlelr */
      __syscall0: function __syscall0(n) { return syscall(instance, n, []); },
      __syscall1: function __syscall1(n, a) { return syscall(instance, n, [a]); },
      __syscall2: function __syscall2(n, a, b) { return syscall(instance, n, [a, b]); },
      __syscall3: function __syscall3(n, a, b, c) { return syscall(instance, n, [a, b, c]); },
      __syscall4: function __syscall4(n, a, b, c, d) { return syscall(instance, n, [a, b, c, d]); },
      __syscall5: function __syscall5(n, a, b, c, d, e) { return syscall(instance, n, [a, b, c, d, e]); },
      __syscall6: function __syscall6(n, a, b, c, d, e, f) { return syscall(instance, n, [a, b, c, d, e, f]); },

      putc_js: function (c) {
        console.log('Sent >> '  +String(c))
        c = String.fromCharCode(c);
        if (c == "\n") {
          console.log(wasm_stdout);
          wasm_stdout  = "";
        } else {
          wasm_stdout += c;
        }
      }
    }
  })
).then(results => {
    instance = results.instance;

    let a = new Uint8Array([
        0xE4, 0x47, 0x30, 0x10, 0x61, 0x24, 0x52, 0x21, 0x86, 0x40, 0xAD, 0xC1, 0xA0, 0xB4, 0x50, 0x22, 0xD0, 0x75, 0x32, 0x48, 0x24, 0x86, 0xE3, 0x48, 0xA1, 0x85, 0x36, 0x6D, 0xCC, 0x33, 0x7B, 0x6E, 0x93, 0x7F, 0x73, 0x61, 0xA0, 0xF6, 0x86, 0xEA, 0x55, 0x48, 0x2A, 0xB3, 0xFF, 0x6F, 0x91, 0x90, 0xA1, 0x93, 0x70, 0x7A, 0x06, 0x2A, 0x6A, 0x66, 0x64, 0xCA, 0x94, 0x20, 0x4C, 0x10, 0x61, 0x53, 0x77, 0x72, 0x42, 0xE9, 0x8C, 0x30, 0x2D, 0xF3, 0x6F, 0x6F, 0xB1, 0x91, 0x65, 0x24, 0x0A, 0x14, 0x21, 0x42, 0xA3, 0xEF, 0x6F, 0x55, 0x97, 0xD6

        //0xB6, 0xFF, 0x65, 0xC3, 0xED, 0x7E, 0xA4, 0x00,
        //                     0x61, 0xD3, 0xFF, 0x72, 0x36, 0x02, 0x67, 0x91,
        //0xD2, 0xD5, 0xC8, 0xA7, 0xE0, 0x6E
    ]);

    //let b = new Uint8Array(new TextEncoder().encode('\x00\xe4\x00G\x000\x00\x10\x00a\x00$\x00R\x00!\x00\x86\x00@\x00\xad\x00\xc1\x00\xa0\x00\xb4\x00P\x00"\x00\xd0\x00u\x002\x00H\x00$\x00\x86\x00\xe3\x00H\x00\xa1\x00\x85\x006\x00m\x00\xcc\x003\x00{\x00n\x00\x93\x00\x7f\x00s\x00a\x00\xa0\x00\xf6\x00\x86\x00\xea\x00U\x00H\x00*\x00\xb3\x00\xff\x00o\x00\x91\x00\x90\x00\xa1\x00\x93\x00p\x00z\x00\x06\x00*\x00j\x00f\x00d\x00\xca\x00\x94\x00 \x00L\x00\x10\x00a\x00S\x00w\x00r\x00B\x00\xe9\x00\x8c\x000\x00-\x00\xf3\x00o\x00o\x00\xb1\x00\x91\x00e\x00$\x00\n\x00\x14\x00!\x00B\x00\xa3\x00\xef\x00o\x00U\x00\x97\x00\xd6'));
    let b = new Uint8Array(new TextEncoder().encode(getParameterByName("q")));

    //let b=  new Uint8Array([0, 228, 0, 71, 0, 48, 0, 16, 0, 97, 0, 36, 0, 82, 0, 33, 0, 134, 0, 64, 0, 173, 0, 193, 0, 160, 0, 180, 0, 80, 0, 34, 0, 208, 0, 117, 0, 50, 0, 72, 0, 36, 0, 134, 0, 227, 0, 72, 0, 161, 0, 133, 0, 54, 0, 109, 0, 204, 0, 51, 0, 123, 0, 110, 0, 147, 0, 127, 0, 115, 0, 97, 0, 160, 0, 246, 0, 134, 0, 234, 0, 85, 0, 72, 0, 42, 0, 179, 0, 255, 0, 111, 0, 145, 0, 144, 0, 161, 0, 147, 0, 112, 0, 122, 0, 6, 0, 42, 0, 106, 0, 102, 0, 100, 0, 202, 0, 148, 0, 32, 0, 76, 0, 16, 0, 97, 0, 83, 0, 119, 0, 114, 0, 66, 0, 233, 0, 140, 0, 48, 0, 45, 0, 243, 0, 111, 0, 111, 0, 177, 0, 145, 0, 101, 0, 36, 0, 10, 0, 20, 0, 33, 0, 66, 0, 163, 0, 239, 0, 111, 0, 85, 0, 151, 0, 214]
    //);

    let pa = wasm_alloc(instance, 0x200);
    wasm_write(instance, pa, a);

    let pb = wasm_alloc(instance, 0x200);
    wasm_write(instance, pb, b);

    if (instance.exports.Match(pa, a.byteLength, pb, b.byteLength) == 1) {
        // PARTY POPPER
        document.getElementById("container").innerText = "🎉";
    } else {
        // PILE OF POO
        document.getElementById("container").innerText = "💩";
    }
});
