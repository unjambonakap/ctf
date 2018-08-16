#include"helper.h"

const uchar *m64;
int rm64[128];
double freq[]={12.02,9.10,8.12,7.68,7.31,6.95,6.28,6.02,5.92,4.32,3.98,2.88,2.71,2.61,2.30,2.11,2.09,2.03,1.82,1.49,1.11,0.69,0.17,0.11,0.10,0.07,0};
int sfreq[27];

int cmp1(int a, int b){return freq[a]>freq[b];}
double sq(double a){return a*a;}

void inithelper(){
    m64=(uchar*)"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    REP(i,64) rm64[m64[i]]=i;

    REP(i,27) sfreq[i]=i;
    sort(sfreq,sfreq+27,cmp1);
}


void genivkey(buffer &iv, AES_KEY *key, AES_KEY *rkey){
    iv=buffer::Rand(16);
    buffer kk=buffer::Rand(16);
    AES_set_encrypt_key(kk.a,16*8,key);
    AES_set_decrypt_key(kk.a,16*8,rkey);

}
buffer buffer::tob64() const{
    int sz=(n+2)*4/3+2;
    buffer b(sz+n+10);

    uchar *A=b.a+sz;
    memcpy(b.a+sz,a,n);

    int pad=(3-n%3)%3, m=0;
    for (int i=0; i<n+pad; i+=3){
        int x=A[i]<<16|A[i+1]<<8|A[i+2];
        REP(j,4) b.a[m+3-j]=m64[x&0x3f], x>>=6;
        m+=4;
    }
    REP(i,pad) b.a[m++]='=';
    b.a[m]=0;
    b.n=m;
    return b;
}

buffer buffer::fromb64() const{
    int pad=0;
    for (;a[n-pad-1]=='='; ++pad);
    int sz=(n+3)*3/4-pad+10;
    buffer b(sz);

    int m=0;
    for (int i=0; i<n-pad;){
        int x=0;
        REP(j,4) x=x<<6|rm64[a[i++]];
        REP(j,3) b.a[m+2-j]=x&0xff, x>>=8;
        m+=3;
    }
    m-=pad;
    b.n=m;
    return b;
}


buffer readfile(uchar *fname){
    buffer a(111111);
    int n=0;
    FILE *f=fopen((char*)fname,"r");
    while(fscanf(f," %s",(char*)a.a+n)>0) n+=strlen((char*)a.a+n);
    assert(n<11111);
    fclose(f);
    a.n=n;
    return a;
}

vector<buffer> readfilebyline(uchar *fname){
    vector<buffer> res;

    buffer a(11111);
    FILE *f=fopen((char*)fname,"r");
    assert(f);
    while(fscanf(f," %s",(char*)a.a)>0){
        a.n=strlen((char*)a.a);
        res.pb(a.copy());
    }
    fclose(f);
    return res;
}



buffer aes_ecb_encrypt(const buffer &in, AES_KEY *key, int bs){
    buffer tmp=in.pkcs7(bs);
    buffer out=buffer(tmp.n);
    REP(i,tmp.n/bs) AES_ecb_encrypt(in.a+i*bs,out.a+i*bs,key,AES_ENCRYPT);
    return out;
}

buffer aes_cbc_encrypt(const buffer &in, const buffer &iv, AES_KEY *key, int bs){
    buffer tmp=in.pkcs7(bs);
    buffer out=buffer(tmp.n);
    buffer iv2(iv);
    AES_cbc_encrypt(tmp.a,out.a,tmp.n,key,iv2.a,AES_ENCRYPT);
    return out;
}

buffer aes_ecb_decrypt(const buffer &in, AES_KEY *key, int bs){
    buffer out(in.n);
    REP(i,in.n/bs) AES_ecb_encrypt(in.a+i*bs,out.a+i*bs,key,AES_DECRYPT);
    out.rpkcs7();
    return out;
}

buffer aes_cbc_decrypt(const buffer &in, const buffer &iv, AES_KEY *key, int bs){
    buffer iv2(iv);
    buffer out(in.n);
    AES_cbc_encrypt(in.a,out.a,in.n,key,iv2.a,AES_DECRYPT);
    out.rpkcs7();
    return out;
}



buffer ctr_go(const buffer &in, const buffer &keys, ll nonce){
    int bs=16;
    int n=in.n;
    buffer out(in);
    buffer ks(bs), tmp(bs);
    AES_KEY key;
    AES_set_encrypt_key(keys.a,bs*8,&key);
    memcpy(tmp.a,&nonce,8);

    REP(i,(n+15)/16){
        memcpy(tmp.a+8,&i,4);
        AES_encrypt(tmp.a,ks.a,&key);
        int u=min(n-i*16,16);
        REP(j,u) out.a[i*bs+j]^=ks.a[j];
    }
    return out;
}


double buffer::computescore()const{
    map<int,int> mp;
    int nx=n;
    REP(i,n) if (isalpha(a[i])) ++mp[a[i]|32], --nx;

    int nsp=0;
    REP(i,n) if (isprint(a[i]) && isspace(a[i])) ++nsp, --nx;

    double sc=0;
    sc+=sq(100.*nsp/n-freq[sfreq[0]]);
    FE(it,mp) sc+=sq(freq[it->ST-'a']-100.*it->ND/n);
    sc+=sq(100.*nx/n);
    return sc;
}

buffer xorstream::go(){

    n=tb.size();
    mx=0;
    REP(i,n) mx=max(mx,tb[i].n);
    buffer res(mx);
    vector<pair<double,uchar> > lst[mx];

    assert(n<maxn);

    REP(i,n) perm[i]=i;
    sort(perm,perm+n,cmpbuffervector(tb));
    reverse(perm,perm+n);
    REP(i,n) iperm[perm[i]]=i;


    buffer x(n);
    REP(i,mx){
        REP(j,n) x[j]=tb[j][i];
        REP(v,256){
            REP(j,n) x[j]^=v;
            lst[i].pb(MP(x.computescore(),v));
            REP(j,n) x[j]^=v;
        }
        sort(ALL(lst[i]));
        state[i]=lst[i][0].ND;
    }

    dispstate();
    while(1){
        printf("want to modify? (row,col,value)\n");
        int a,b;
        char c;
        if (scanf(" %d%d %c",&a,&b,&c)<=0) break;
        if (a==-1) break;
        if (a<0 || a>=n){puts("bad row index");}
        else if (b<0 || b>=tb[perm[a]].n) puts("bad col index");
        else{
            state[b]=tb[perm[a]][b]^c;
            dispstate();
        }

    }
    dispstate();
    REP(i,n) res[i]=state[i];
    return res;
}


void xorstream::dispstate(){

    printf("    ");
    REP(i,mx){
        if (i%10) printf(" ");
        else i+=printf("%d",i)-1;
    }
    puts("");
    printf("    ");
    REP(i,mx) printf("%d",i%10);
    puts("");

    REP(_i,n){
        int i=perm[_i];
        printf("%2d>>",_i);
        REP(j,min(mx,tb[i].n)){
            uchar c=tb[i][j]^state[j];
            if (state[j]==-1) c='?';
            printf("%c",isprint(c)?c:'#'); 
        }
        puts("<<<EOF");
    }
    printf("    ");
    REP(i,mx){
        if (i%10) printf(" ");
        else i+=printf("%d",i)-1;
    }
    puts("");
    printf("    ");
    REP(i,mx) printf("%d",i%10);
    puts("");

}

void xorstream::dispresult(){
    puts(""); puts(""); puts("");
    printf("STREAM >>>\n");
    REP(i,n) printf("%02x",state[i]);
    printf("TEXT RESULT\n");
    dispstate();
}



buffer sha1(const buffer &a){
    buffer res(20);
    SHA1(a.a,a.n,res.a);
    return res;
}

buffer sha1_prefix(const buffer &key, const buffer &a){
    buffer tmp=key+"#"+a;
    buffer res(20);
    SHA1(tmp.a,tmp.n,res.a);
    return res;
}


void sha1_hashtoctx(const buffer &hash, SHA_CTX *ctx){
    SHA1_Init(ctx);
    if (hash.n==20) REP(j,5) *((int*)&ctx->h0+j)=htobe32(*((int*)hash.a+j));
    else assert(!hash.n);
}

buffer sha1_ctxtohash(SHA_CTX *ctx){
    buffer hash(20);
    REP(j,5) *((int*)hash.a+j)=htobe32(*((int*)&ctx->h0+j));
    return hash;
}

buffer sha1_raw(const buffer &a, SHA_CTX *ctx){
    buffer res(20);
    assert(a.n%64==0);
    REP(i,a.n/64) SHA1_Transform(ctx,a.a+i*64);
    return sha1_ctxtohash(ctx);
}
buffer sha1_raw(const buffer &a, const buffer &prev){
    SHA_CTX ctx;
    sha1_hashtoctx(prev,&ctx);
    return sha1_raw(a,&ctx);
}

buffer sha1_preproc(const buffer &a, int cursz, int sz){
    cursz+=a.n;
    sz+=cursz;
    int l=448-8*cursz&0x1ff;
    buffer b(a.n+l/8+8);
    memcpy(b.a,a.a,a.n);
    b[a.n]=0x80;
    *((ull*)(b.a+b.n)-1)=htobe64(8ll*sz);
    return b;
}





buffer md4(const buffer &a){
    buffer res(16);
    MD4_CTX ctx;
    MD4_Init(&ctx);
    MD4_Update(&ctx,a.a,a.n);
    printf("%x %x %x %x\n",ctx.A,ctx.B,ctx.C,ctx.D);
    MD4_Final(res.a,&ctx);
    //MD4(a.a,a.n,res.a);
    return res;
}

buffer md4_prefix(const buffer &key, const buffer &a){
    buffer tmp=key+"#"+a;
    buffer res(16);
    MD4(tmp.a,tmp.n,res.a);
    return res;
}


void md4_hashtoctx(const buffer &hash, MD4_CTX *ctx){
    MD4_Init(ctx);
    if (hash.n==16) REP(j,4) *((int*)&ctx->A+j)=htole32(*((int*)hash.a+j));
    else assert(!hash.n);
}

buffer md4_ctxtohash(MD4_CTX *ctx){
    buffer hash(16);
    REP(j,4) *((int*)hash.a+j)=htole32(*((int*)&ctx->A+j));
    return hash;
}

buffer md4_raw(const buffer &a, MD4_CTX *ctx){
    buffer res(16);
    assert(a.n%64==0);
    REP(i,a.n/64){
        MD4_Transform(ctx,a.a+i*64);
        printf("%x %x %x %x\n",ctx->A,ctx->B,ctx->C,ctx->D);
    }
    return md4_ctxtohash(ctx);
}
buffer md4_raw(const buffer &a, const buffer &prev){
    MD4_CTX ctx;
    md4_hashtoctx(prev,&ctx);
    return md4_raw(a,&ctx);
}

buffer md4_preproc(const buffer &a, int cursz, int sz){
    cursz+=a.n;
    sz+=cursz;
    int l=448-8*cursz&0x1ff;
    buffer b(a.n+l/8+8);
    memcpy(b.a,a.a,a.n);
    b[a.n]=0x80;
    *((ull*)(b.a+b.n)-1)=htole64(8ll*sz);//fuk you little endian
    return b;
}

buffer hmac(const buffer &a, const buffer &key){
    HMAC_CTX ctx;
    HMAC_CTX_init(&ctx);
    buffer res(200);
    HMAC(EVP_sha1(),key.a,key.n,a.a,a.n,res.a,(uint*)&res.n);
    return res;
}
char gethexchar(int x){return x<=9?x+'0':x-10+'a';}

buffer sha256(const buffer &a){
    buffer res(32);
    SHA256(a.a,a.n,res.a);
    return res;
}

buffer hmac256(const buffer &a, const buffer &key){
    HMAC_CTX ctx;
    HMAC_CTX_init(&ctx);
    buffer res(200);
    HMAC(EVP_sha256(),key.a,key.n,a.a,a.n,res.a,(uint*)&res.n);
    return res;
}
