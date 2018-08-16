import web
from time import *;
import hmac;
from hashlib import sha1;

urls = (
    '/test', 'test'
)
key="jeez i need to learn python";

def lame_compare(a,b):
    if (len(a)!=len(b)):
        return 0;

    for i in range(len(a)):
        sleep(1e-3);
        if (a[i]!=b[i]):
            return 0;
    return 1;



class test:
    def GET(self):
        u=web.input();
        if ("file" in u and "signature" in u):
            a=u.file;
            b=u.signature;
            res=hmac.new(key,a,sha1).digest().encode('hex');
            print b;
            print res;

            return lame_compare(b,res);
        return "missing args";

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
