#include "BigNum.h"


#define REP(i,n) for(i = 0; i < (n); i++)
#define REPC(i,n,c) for(i = 0; (i < (n)) && (c); i++)

#define REPV(i, n) for (i = (n) - 1; i >= 0; i--)
#define REPVC(i, n, c) for (i = (n) - 1; (i >= 0) && (c); i--)
#define FOR(i, a, b) for(i = (a); i <= (b); i++)
#define FORC(i, a, b, c) for(i = (a); (i <= (b)) && (c); i++)
#define FORV(i, a, b) for(i = (a); i >= (b); i--)
#define FORVC(i, a, b, c) for(i = (a); (i >= (b)) && (c); i--)
#define FE(i,t) for (typeof(t.begin())i=t.begin();i!=t.end();i++)
#define FEV(i,t) for (typeof(t.rbegin())i=t.rbegin();i!=t.rend();i++)

#define MAX(a,b) (((a) < (b)) ? (b) : (a))
#define MIN(a,b) (((a) < (b)) ? (a) : (b))
#define pb push_back
#define ST first
#define ND second
#define SZ(a) (int((a).size()))
#define two(x) (1 << (x))
#define twoll(x) (1LL << (x))
#define ALL(a) (a).begin(), (a).end()
#define CLR(a) (a).clear()
#define SWAP(a,b,c) (c=a, a=b, b=c)

#define MP(x, y) make_pair(x, y)
#define SQR(x) (pow((x),2))
#define DIST(x,y) (SQR(x)+SQR(y))
#define MDIST(x,y,a,b) (abs((a)-(x))+abs((b)-(y)))

#define CMP(x,y) ((fabs((x)-(y)) < EPS) ? 0 : ((x) < (y)) ? -1 : 1)


inline int count_bit(int n){return (n == 0)?0:1+count_bit(n&(n-1));}
inline ll sqr(int x){return ll(x)*ll(x);}
inline double dist(ll x, ll y, ll a, ll b){return sqrt(double(sqr(x-a)+sqr(y-b)));}
inline bool bit_set(int a, int b){return (a&two(b));}

const double INF=1e20;

ostream& operator<<(ostream& o, const BigNum& a){ o<<a.getStr(10); return o; }

namespace BigNumUtils{

	BigNum sqr(const BigNum& x){return x*x;}
	
	BigNum genNumLE(const BigNum& a){
		string s, os; int i;
		bool inf=false;

		os=a.getStr();
		s+='0'+rand()%(os[0]-'0'+1);

		if (os[0]>s[0]) inf=true;

		FOR(i, 1, os.length()-1)
			s+='0'+rand()%((inf)?10:(os[i]-'0'+1)), inf|=os[i]>s[i];
		return BigNum(s);
	}

	BigNum genNumB(const BigNum& a, const BigNum& b){ BigNum c(a);return c+genNumLE(b-a); }


	bool isPrimeRB(const BigNum& n, int np){
		int i;
		REP(i, np)
			if (rbTest(n) == false)return false;
		return true;
	}


	bool rbTest(const BigNum& n){//rabin-Miller primality test
		//assertion n>2
		int i, k;
		BigNum t(n-1);
		k=t.ctz();

		BigNum m(n>>k), a(genNumB(2, n-1));
		assert(!m.isEven());

		a.spowm(m, n);
		if (a==1)return true;
		REP(i, k){
			if (a==t)return true;
			a.spowm(2, n);
		}
		return false;
	}

	BigNum genNum(long int a){
		string s; int i;

		s+='0'+rand()%9+1;
		FOR(i, 1, a-1)
			s+='0'+rand()%10;
		return BigNum(s);
	}

	BigNum genOdd(long int a){
		string s; int i;

		s+='0'+rand()%9+1;
		FOR(i, 1, a-2)
			s+='0'+rand()%10;
		s+='0'+(rand()%5)*2+1;

		return BigNum(s);
	}
	BigNum genPrime(long int a){
		BigNum b;
		while(1){
			b=genOdd(a);
			if (isPrimeRB(b))
				return b;
		}
	}


	int jacobi(const BigNum& a, const BigNum& b){
		BigNum x(a), y(b);
		return _jacobi(x, y);
	}

	int _jacobi(BigNum a, BigNum b){
		int p, sgn=1;


		if (b==1 || a==1)return 1;
		if (a==0)return 0;
		if (a==2)
			return ((p=(b%8).getSi())==1 || p==7)?1:-1;
		

		a%=b;
		if (a==0)return 0;
		p=a.ctz();

		if (p != 0){
			a>>=p;
			sgn*=pow(jacobi(2, b), p);
		}

		//a odd
		if (a%4==3 && b%4==3)
			sgn*=-1;
		p=jacobi(b, a);
		return p*sgn;
	}

	int __jacobi(const BigNum &a, const BigNum& b){ return mpz_jacobi(const_cast<BigNum&>(a).n, const_cast<BigNum&>(b).n); }




	BigNum _gcd(BigNum& a, BigNum& b){
		//cout<<a<<endl;
		//cout<<b<<endl<<endl;
		BigNum c(a%b);
		if (c==0)return b;
		return _gcd(b, c);
	}

	BigNum gcd(const BigNum& a, const BigNum& b){
		BigNum c(a), d(b);
		if (a==0||b==0)return max(a, b);
		if (c < d) return _gcd(d, c);
		return _gcd(c, d);
	}

	BigNum __gcd(const BigNum& a, const BigNum& b){
		BigNum c, x(a), y(b);
		mpz_gcd(c.n, x.n, y.n);
		return c;
	}

	BigNum _bezoutDc(const BigNum& a, const BigNum& b, BigNum& u, BigNum& v){
		BigNum c(a%b), t;
		if (c==0){
			u=0, v=1;
			return b;
		}
		
		BigNum d(_bezoutDc(b, c, u, v));

		t=u, u=v, v=t-(a/b)*v;
		return d;
	}


	void bezoutDc(const BigNum& a, const BigNum& b, BigNum& d, BigNum& u, BigNum& v){
		BigNum x(a), y(b);
		if (x < y)
			d=_bezoutDc(y, x, v, u);
		else
			d=_bezoutDc(x, y, u, v);

	}

	vector<BigNum> bezoutDct(const BigNum& a, const BigNum& b){
		BigNum x, y, z;
		vector<BigNum> v;
		bezoutDc(a, b, z, x, y);
		v.pb(z), v.pb(x), v.pb(y);
		return v;
	}

	void gcdext(const BigNum& a, const BigNum& b, BigNum& d, BigNum& u, BigNum& v){ 
		BigNum x(a), y(b);
		mpz_gcdext(d.n, u.n, v.n, x.n, y.n); 
	}

	vector<BigNum> gcdextt(const BigNum& a, const BigNum& b){
		BigNum x, y, z;
		vector<BigNum> v;
		gcdext(a, b, z, x, y);
		v.pb(z), v.pb(x), v.pb(y);
		return v;
	}


	BigNum sqrt(const BigNum& a){
		BigNum b(a);
		mpz_sqrt(b.n, a.getMpz());
		return b;
	}

	BigNum root(const BigNum &a, int n){
		BigNum b(a);
		mpz_root(b.n, a.getMpz(), n);
		return b;
	}

	BigNum inv(const BigNum& x, const BigNum& n){return x.inv(n);}
	int log2a(BigNum n){ return n.log2(); }

	bool isCoprime(const BigNum& a, const BigNum& b){ return __gcd(a, b)==1; }
}
/*======================++++BigNum class======================================*/

BigNum::BigNum(ull a){
	char buf[100];
	sprintf(buf, "%Lu", a);
	mpz_init(n), mpz_init(r);
	mpz_set_str(n, buf, 10);

}
BigNum::BigNum(const BigNum& a){
	mpz_init(n), mpz_init(r);
	mpz_set(n, a.n);
}

BigNum::BigNum(long int a){
	mpz_init(n);
	mpz_init(r);
	mpz_set_si(n, a);
}
BigNum::BigNum(unsigned long int a){
	mpz_init(n);
	mpz_init(r);
	mpz_set_ui(n, a);
}
BigNum::BigNum(int a){
	mpz_init(n);
	mpz_init(r);
	mpz_set_si(n, a);
}

BigNum::BigNum(double a){
	mpz_init(n);
	mpz_init(r);
	mpz_set_d(n, a);
}

BigNum::BigNum(const string& s, int b){
	mpz_init(n);
	mpz_init(r);
	mpz_set_str(n, s.c_str(), b);
}

BigNum::BigNum(const char *s, int b){
	mpz_init(n);
	mpz_init(r);
	mpz_set_str(n, s, b);
}
BigNum::BigNum(const mpz_t a){
	mpz_init(n);
	mpz_init(r);
	mpz_set(n, a);
}

BigNum::~BigNum(){ mpz_clear(n), mpz_clear(r); }


void BigNum::swap(BigNum &a){ mpz_swap(a.n, this->n); }

BigNum& BigNum::operator=(const BigNum& a){
	mpz_set(n, a.n);
	return *this;
}

//comparison operators

bool BigNum::operator<(const BigNum& a)const{return mpz_cmp(n, a.n)<0;}
bool BigNum::operator>(const BigNum& a)const{return mpz_cmp(n, a.n)>0;}
bool BigNum::operator<=(const BigNum& a)const{return mpz_cmp(n, a.n)<=0;}
bool BigNum::operator>=(const BigNum& a)const{return mpz_cmp(n, a.n)>=0;}
bool BigNum::operator==(const BigNum& a)const{return mpz_cmp(n, a.n)==0;}
bool BigNum::operator!=(const BigNum& a)const{return mpz_cmp(n, a.n)!=0;}





// axy operators
const BigNum BigNum::operator*(const BigNum& a)const{
	BigNum c;
	mpz_mul(c.n, n, a.n);
	return c;
}
const BigNum BigNum::operator+(const BigNum& a)const{
	BigNum c;
	mpz_add(c.n, n, a.n);
	return c;

}
const BigNum BigNum::operator-()const{
	BigNum c;
	mpz_neg(c.n, n);
	return c;

}
const BigNum BigNum::operator-(const BigNum& a)const{
	BigNum c;
	mpz_sub(c.n, n, a.n);
	return c;

}
const BigNum BigNum::operator/(const BigNum& a)const{
	BigNum c;
	mpz_fdiv_q(c.n, n, a.n);
	return c;
}
const BigNum BigNum::operator%(const BigNum& a)const{
	BigNum c;
	mpz_mod(c.n, n, a.n);
	return c;
}

const BigNum BigNum::operator^(const unsigned long int& e)const{
	BigNum c;
	mpz_pow_ui(c.n, n, e);
	return c;
}

const BigNum BigNum::powm(const BigNum& a, const BigNum& b)const{
	BigNum c;
	mpz_powm(c.n, n, a.n, b.n);
	return c;
}

const BigNum BigNum::operator&(const BigNum& a)const{
	BigNum c;
	mpz_and(c.n, n, a.n);
	return c;
}

const BigNum BigNum::operator|(const BigNum& a)const{
	BigNum c;
	mpz_ior(c.n, n, a.n);
	return c;
}

const BigNum BigNum::operator<<(const int& a)const{
	string s=this->getStr(2);
	s.append('0', a);
	return BigNum(s, 2);
}

const BigNum BigNum::operator>>(const int& a)const{
	string s=this->getStr(2);
	s.erase(s.length()-a);
	return BigNum(s, 2);
}

const BigNum BigNum::mxor(const BigNum& a)const{
	BigNum c;
	mpz_xor(c.n, n, a.n);
	return c;
}

const ull BigNum::popcount()const{ return mpz_popcount(n); }

const ull BigNum::ctz()const{
	string s=this->getStr(2);
	int i;
	REPV(i, s.length())
		if (s[i] == '1')return s.length()-i-1;
	return -1;
}

int BigNum::sizeInBase(int a)const{return mpz_sizeinbase(n, a);}



//========================== x= operators==============
BigNum& BigNum::operator*=(const BigNum& a){
	mpz_mul(n, n, a.n);
	return *this;
}

BigNum& BigNum::operator+=(const BigNum& a){
	mpz_add(n, n, a.n);
	return *this;
}

BigNum& BigNum::operator-=(const BigNum& a){
	mpz_sub(n, n, a.n);
	return *this;
}
BigNum& BigNum::operator/=(const BigNum& a){
	mpz_fdiv_q(n, n, a.n);
	return *this;
}

BigNum& BigNum::operator%=(const BigNum& a){
	mpz_mod(n, n, a.n);
	return *this;
}

BigNum& BigNum::operator^=(const unsigned long int& e){
	mpz_pow_ui(n, n, e);
	return *this;
}


BigNum& BigNum::spowm(const BigNum& a, const BigNum& b){
	mpz_powm(n, n, a.n, b.n);
	return *this;
}

BigNum& BigNum::operator++(){
	mpz_add_ui(n, n, 1);
	return *this;
}
BigNum& BigNum::operator--(){
	mpz_sub_ui(n, n, 1);
	return *this;
}


BigNum BigNum::operator++(int){
	BigNum b=*this;
	mpz_add_ui(n, n, 1);
	return b;
}
BigNum BigNum::operator--(int){
	BigNum b=*this;
	mpz_sub_ui(n, n, 1);
	return b;
}

BigNum& BigNum::operator&=(const BigNum& a){
	mpz_and(n, n, a.n);
	return *this;
}
BigNum& BigNum::operator|=(const BigNum& a){
	mpz_ior(n, n, a.n);
	return *this;
}
BigNum& BigNum::sxor(const BigNum& a){
	mpz_xor(n, n, a.n);
	return *this;
}

BigNum& BigNum::operator<<=(const int& a){
	string s=this->getStr(2);
	s.append(a, '0');
	mpz_set_str(n, s.c_str(), 2);

	return *this;
}


BigNum& BigNum::operator>>=(const int& a){
	string s=this->getStr(2);
	s.erase(s.length()-a);
	mpz_set_str(n, s.c_str(), 2);

	return *this;
}


const BigNum BigNum::exDiv(const BigNum& a)const{
	BigNum c;
	mpz_divexact(c.n, n, a.n);
	return c;
}
BigNum& BigNum::sexDiv(const BigNum& a){
	mpz_divexact(n, n, a.n);
	return *this;
}


unsigned long int BigNum::modUi(unsigned long int a)const{ return mpz_fdiv_ui(n, a); }

BigNum BigNum::inv(const BigNum& n)const{ return BigNumUtils::gcdextt(*this, n)[1]%n; }

string BigNum::getStr(int b)const{
	char *buf;
	buf=mpz_get_str(NULL, b, n);

	string s(buf);
	free(buf);
	return s;
}

long int BigNum::getSi()const{return mpz_get_si(n);}
unsigned long int BigNum::toUi()const{return mpz_get_ui(n);}
mpz_t& BigNum::getMpz(){return n;}
const mpz_t& BigNum::getMpz()const{return n;}



bool BigNum::isEven()const{return mpz_even_p(n);}

int BigNum::nDigit(int b)const{ return getStr(b).length(); } 
int BigNum::log2()const{return sizeInBase(2);}



