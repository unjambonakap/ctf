#ifndef BIGNUM_H
#define BIGNUM_H 

#include <vector>
#include <list>
#include <map>
#include <set>
#include <deque>
#include <queue>
#include <stack>
#include <algorithm>
#include <numeric>
#include <utility>
#include <iostream>
#include <cstdlib>
#include <string>
#include <cstring>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <cassert>
#include <climits>
//#include <ext/hash_map>
#include <gmp.h>
#include <mpfr.h>


using namespace std;
using namespace __gnu_cxx;

typedef long long ll;
typedef unsigned long long ull;
typedef pair<int,int> pii;
typedef vector<int> vi;
typedef vector<string> vs;
typedef queue<int> qi;

class BigNum;

typedef vector<vector<BigNum> > MBN;
ostream& operator<<(ostream&, const BigNum&);

namespace BigNumUtils{


	BigNum genNum(long int);
	BigNum genNumLE(const BigNum&);
	BigNum genNumB(const BigNum&, const BigNum&);

	BigNum genOdd(long int);
	BigNum genPrime(long int);

	bool rbTest(const BigNum&);
	bool isPrimeRB(const BigNum&, int=100);




	BigNum gcd(const BigNum&, const BigNum&);
	BigNum _gcd(BigNum&, BigNum&);
	BigNum __gcd(const BigNum&, const BigNum&);

	BigNum _bezoutDc(const BigNum&, const BigNum&, BigNum&, BigNum&);
	void bezoutDc(const BigNum&, const BigNum&, BigNum&, BigNum&, BigNum&);
	vector<BigNum> bezoutDct(const BigNum&, const BigNum&);

	void gcdext(const BigNum&, const BigNum&, BigNum&, BigNum&, BigNum&);
	vector<BigNum> gcdextt(const BigNum&, const BigNum&);

	int jacobi(const BigNum&, const BigNum&);
	int _jacobi(BigNum, BigNum);
	int __jacobi(const BigNum&, const BigNum&);

	BigNum sqrt(const BigNum&);
	BigNum root(const BigNum&, int n);
	BigNum sqr(const BigNum&);
	BigNum inv(const BigNum&, const BigNum&);
	double log(BigNum);
	bool isCoprime(const BigNum&, const BigNum&);


};

class BigNum{
	public:
		friend void BigNumUtils::gcdext(const BigNum&, const BigNum&, BigNum&, BigNum&, BigNum&);
		friend BigNum BigNumUtils::__gcd(const BigNum&, const BigNum&);
		friend int BigNumUtils::__jacobi(const BigNum&, const BigNum&);

		BigNum(long int);
		BigNum(unsigned long int);
		BigNum(ull);
		BigNum(int=0);
		BigNum(double);
		BigNum(const mpz_t);
		BigNum(const string&, int=10);
		BigNum(const char*, int=10);
		BigNum(const BigNum&);
		void swap(BigNum&);

		BigNum& operator=(const BigNum&);

		bool operator<(const BigNum&)const;
		bool operator>(const BigNum&)const;
		bool operator<=(const BigNum&)const;
		bool operator>=(const BigNum&)const;
		bool operator==(const BigNum&)const;
		bool operator!=(const BigNum&)const;


		const BigNum operator*(const BigNum&)const;
		const BigNum operator+(const BigNum&)const;
		const BigNum operator-()const;
		const BigNum operator-(const BigNum&)const;
		const BigNum operator/(const BigNum&)const;
		const BigNum operator%(const BigNum&)const;
		const BigNum operator^(const unsigned long int&)const;

		const BigNum operator&(const BigNum&)const;
		const BigNum operator|(const BigNum&)const;
		const BigNum operator<<(const int&)const;
		const BigNum operator>>(const int&)const;
		const BigNum mxor(const BigNum&)const;
		const ull popcount()const;
		const ull ctz()const;
		int sizeInBase(int=2)const;
		int log2()const;

		const BigNum powm(const BigNum&, const BigNum&)const;
		BigNum& spowm(const BigNum&, const BigNum&);
		BigNum& operator*=(const BigNum&);
		BigNum& operator+=(const BigNum&);
		BigNum& operator-=(const BigNum&);
		BigNum& operator/=(const BigNum&);
		BigNum& operator%=(const BigNum&);
		BigNum& operator^=(const unsigned long int&);
		BigNum& operator&=(const BigNum&);
		BigNum& operator|=(const BigNum&);
		BigNum& operator<<=(const int&);
		BigNum& operator>>=(const int&);
		BigNum& sxor(const BigNum&);

		BigNum& operator++();
		BigNum& operator--();
		BigNum operator++(int);
		BigNum operator--(int);
		BigNum inv(const BigNum&)const;

		const BigNum exDiv(const BigNum&)const;
		BigNum& sexDiv(const BigNum&);
		unsigned long int modUi(unsigned long int)const;


		string getStr(int=10) const;
		long int getSi()const;
		unsigned long int toUi()const;
		mpz_t& getMpz();
		const mpz_t& getMpz()const;
		bool isEven()const;
		int nDigit(int=10)const;

		~BigNum();
		

		friend BigNum BigNumUtils::sqrt(const BigNum&);
		friend BigNum BigNumUtils::root(const BigNum&, int);


	private:
		mpz_t n, r;


	
	


};

#endif 

