// MLP2 - TWO-LAYER MULTILAYER PERCEPTRON - SAMPLE IMPLEMENTATION (WITH THE XOR DATA)
// compile: gcc -Wall -std=gnu99 -O3 -ffast-math -funroll-loops -s -o NNRun NNRun.c -lm
// Version 1.0 ----------------------------------------- Copyleft R.JAKSA 2009, GPLv3

#define Nin 2304    // no. of inputs
#define Nh1 3   // no. of hidden units
#define Nou 2   // no. of outputs
#define Gamma 0.2   // learning rate
#define Epochs 10000    // no. of training epochs (cycles)

// ------------------------------------------------------------- END OF CONFIGURATION
#include <math.h>   // fabs, exp
#include <stdlib.h> // rand, srand
#include <stdio.h>  // printf, fgets, sscanf, fopen
#include <sys/timeb.h>  // ftime
#include <string.h> // strtok

#define Nx 1+Nin+Nh1+Nou    // no. of units
#define IN1 1   // 1st input
#define INn Nin // last (n-th) input
#define H11 Nin+1   // 1st hidden
#define H1n Nin+Nh1 // last hidden
#define OU1 Nin+Nh1+1   // 1st output
#define OU2 Nin+Nh1+2   // 2nd output
#define OUn Nin+Nh1+Nou // last output

typedef struct {
    double x[Nx];   // units inputs
    double y[Nx];   // units activations
    double delta[Nx];   // units delta signal
    double w[Nx][Nx];   // weights
    double dv[Nx];  // desired value on output !!! TODO: Nou is enough
} ann_t;

#define w(i,j) ann->w[i][j]
#define x(i) ann->x[i]
#define y(i) ann->y[i]
#define delta(i) ann->delta[i]
#define dv(i) ann->dv[i]

// --------------------------------------- ACTIVATION FUNCTION AND ITS 1st DERIVATION
#define af(X) (1.0/(1.0+exp((-1.0)*(X))))
#define df(X) (exp((-1.0)*(X))/((1.0+exp((-1.0)*(X)))*(1.0+exp((-1.0)*(X)))))

// ---------------------------------------------------------------- MLP2 WEIGHTS INIT
void MLP2_rnd_init(ann_t *ann) {
    y(0)=-1.0;  // the input for bias
    for(int i=0; i<Nx; i++) {
        for(int j=0; j<Nx; j++) {
            w(i,j)=0;   // all weights to zero
        }
    }
}

// ----------------------------------------------------------------- SINGLE LAYER RUN
static void layer_run(ann_t *ann, int i1, int in, int j1, int jn) { // output/input block from-to
    for(int i=i1; i<=in; i++) {
        x(i) = w(i,0) * y(0);   // add bias contribution
        for(int j=j1; j<=jn; j++) {
            x(i) += w(i,j) * y(j);  // add main inputs contrib.
        }
        y(i) = af(x(i));    // apply activation function
    }
}

// ---------------------------------------------------------------------- NETWORK RUN
void MLP2_run(ann_t *ann) {
    layer_run(ann,H11,H1n,IN1,INn); // in -> h1
    layer_run(ann,OU1,OUn,H11,H1n); // h1 -> ou
}

void read_weights_from_file(ann_t *ann, int i1, int in, int j1, int jn, FILE *f_weights) {	// output/input block from-to
    char weights_line[100];
	double weight;
	for(int i=i1; i<=in; i++) {
		fgets(weights_line, 100, f_weights);
		sscanf(weights_line, "%lf", &weight);
		w(i,0) = weight;
        for(int j=j1; j<=jn; j++) {
			fgets(weights_line, 100, f_weights);
            sscanf(weights_line, "%lf", &weight);
            w(i,j) = weight;
        }
    }
}

// ----------------------------------------------------------------------------- MAIN
int main(void) {
	ann_t *ann=(ann_t*)malloc(sizeof(ann_t));
    FILE *f_weights, *f_image;    // file inputs
    char image_line[100];  // one line from image file
    double rgb_value;  // rgb value as number
	
	MLP2_rnd_init(ann);    // initialize the network

    f_weights=fopen("weights.txt", "r");
    if(f_weights == NULL) {
        printf("ERROR: File weights.txt did not open correctly");
        return(1);
    }
	
	read_weights_from_file(ann,H11,H1n,IN1,INn,f_weights);	// in -> h1
    read_weights_from_file(ann,OU1,OUn,H11,H1n,f_weights);	// h1 -> ou
	
    fclose(f_weights);
	
	f_image = fopen("image.txt", "r");
	if(f_image == NULL) {
        printf("ERROR: File image.txt did not open correctly");
        return(1);
    }
	
	int input_index=IN1;
	while (fgets(image_line, 100, f_image) != NULL) {
		sscanf(image_line, "%lf", &rgb_value);
		y(input_index)=rgb_value;   // save rgb value
		input_index++;
	}
	fclose(f_image);
	
	MLP2_run(ann);  // run network

    printf("%f %f", y(OU1), y(OU2));

    free(ann);
	return(0);
}

// ------------------------------------------------------------------------------ END
