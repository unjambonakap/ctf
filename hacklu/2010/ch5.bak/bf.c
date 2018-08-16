#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

const int maxt=10;

int tc[]={1, 2, 3, 30320, 30321, 30322};
int tm[]={30268, 30306};
struct seed{ int a, b; char c; };
struct data{int st, nt, nk;};

void *proc(void *_d){
	data *d=(data*)_d;
	int i, j, k, s, ni, nj, nk, a;
	for (i=d->st; i<tm[0]; i+=d->nt) for (j=0; j<tm[1]; ++j) for (k=0; k<6; ++k){
		ni=i, nj=j, nk=k;
		//INSERT
		ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;

	}

}


int main(int argc, char **argv){
	int nt;
	if (argc<2) nt=2;
	else sscanf(argv[1], "%d", &nt);

	data d[maxt];

	pthread_t th[maxt];

	for (int i=0; i<nt; ++i){
		d[i].st=i, d[i].nt=nt;
		if (pthread_create(th+i, 0, proc, (void*)(d+i))){
			fprintf(stderr, "failed creating thread\n");
			exit(-1);
		}
	}
	void *status;
	for (int i=0; i<nt; ++i){
		if (pthread_join(th[i], &status)){
			fprintf(stderr, "failed joining thread\n");
			exit(-1);
		}
	}
	return 0;

}


