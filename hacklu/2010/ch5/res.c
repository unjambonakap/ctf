#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

const int maxt=10;

int tc[]={1, 2, 3, 30320, 30321, 30322};
int tm[]={30268, 30306};
typedef struct seed{ int a, b; char c; }seed;
typedef struct data{int st, nt, nk;}data;

void *proc(void *_d){
	data *d=(data*)_d;
	int i, j, k, s, ni, nj, nk, a;
	double nr;
	for (i=d->st; i<tm[0]; i+=d->nt) for (j=0; j<tm[1]; ++j) for (k=0; k<6; ++k){

		ni=i, nj=j, nk=tc[k];
		for (a=0; a<18; ++a) ni=(171*ni)%30269, nj=(172*nj)%30307, nk=(170*nk)%30323;


		ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (6!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (6!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (5!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (6!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (2!=(int)(nr*10)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (7!=(int)(nr*10)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (9!=(int)(nr*12)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (7!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (6!=(int)(nr*10)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (3!=(int)(nr*10)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (8!=(int)(nr*12)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (2!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (3!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (1!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (3!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (7!=(int)(nr*10)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (7!=(int)(nr*10)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (6!=(int)(nr*12)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (7!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (3!=(int)(nr*10)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (0!=(int)(nr*10)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (6!=(int)(nr*12)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (0!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (1!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (0!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (7!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (1!=(int)(nr*10)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (5!=(int)(nr*10)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (7!=(int)(nr*12)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (2!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (4!=(int)(nr*10)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (0!=(int)(nr*10)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (5!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (1!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (4!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (5!=(int)(nr*8)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (6!=(int)(nr*10)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (2!=(int)(nr*10)) continue;
ni=(171*ni)%30269; nj=(172*nj)%30307; nk=(170*nk)%30323;
nr=ni/30269.0 + nj/30307.0 + nk/30323.0; nr-=(int)nr;
if (8!=(int)(nr*12)) continue;

		printf("%d %d %d\n", i, j, tc[k]);

	}

}


int main(int argc, char **argv){
	int nt;
	if (argc<2) nt=4;
	else sscanf(argv[1], "%d", &nt);

	data d[maxt];
	int i;

	pthread_t th[maxt];

	for (i=0; i<nt; ++i){
		d[i].st=i, d[i].nt=nt;
		if (pthread_create(th+i, 0, proc, (void*)(d+i))){
			fprintf(stderr, "failed creating thread\n");
			exit(-1);
		}
	}
	void *status;
	for (i=0; i<nt; ++i){
		if (pthread_join(th[i], &status)){
			fprintf(stderr, "failed joining thread\n");
			exit(-1);
		}
	}
	return 0;

}


