// MLP2 - TWO-LAYER MULTILAYER PERCEPTRON - SAMPLE IMPLEMENTATION (WITH THE XOR DATA)
// compile: gcc -Wall -std=gnu99 -O3 -ffast-math -funroll-loops -s -o NNTrain NNTrain.c -lm
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

// -------------------------------------------------------- SINGLE LAYER WEIGHTS INIT
static void layer_rnd_init(ann_t *ann, int i1, int in, int j1, int jn,  // output/input block from-to
                           double min, double max) {    // weights init interval size
    for(int i=i1; i<=in; i++) {
        w(i,0) = rand() / (RAND_MAX/(max-min)) + min;
        for(int j=j1; j<=jn; j++) {
            w(i,j) = rand() / (RAND_MAX/(max-min)) + min;
        }
    }
}

// ---------------------------------------------------------------- MLP2 WEIGHTS INIT
void MLP2_rnd_init(ann_t *ann, double min, double max) {
    y(0)=-1.0;  // the input for bias
    for(int i=0; i<Nx; i++) {
        for(int j=0; j<Nx; j++) {
            w(i,j)=0;   // all weights to zero
        }
    }
    layer_rnd_init(ann,H11,H1n,IN1,INn,min,max);    // in -> h1
    layer_rnd_init(ann,OU1,OUn,H11,H1n,min,max);    // h1 -> ou
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

// ------------------------------------------------------ SINGLE LAYER WEIGHTS UPDATE
static void layer_weights_update(ann_t *ann, int i1, int in, int j1, int jn,    // output/input block from-to
                                 double gamma) {    // learning rate
    for(int i=i1; i<=in; i++) {
        w(i,0) += gamma * delta(i) * y(0);  // bias (weight) update
        for(int j=j1; j<=jn; j++) {
            w(i,j) += gamma * delta(i) * y(j);  // the weights update
        }
    }
}

// ------------------------------------------------- VANILLA BACKPROPAGATION LEARNING
void MLP2_vanilla_bp(ann_t *ann, double gamma) {
    MLP2_run(ann);  // 1st run the network
    for(int i=OU1; i<=OUn; i++) {
        delta(i) = (dv(i)-y(i)) * df(x(i)); // delta on output layer
    }
    for(int i=H11; i<=H1n; i++) {
        double S=0.0;
        for(int h=OU1; h<=OUn; h++) {
            S += delta(h) * w(h,i);
        }
        delta(i) = S * df(x(i));    // delta on hidden layer
    }
    layer_weights_update(ann,OU1,OUn,H11,H1n,gamma);    // h1 -> ou
    layer_weights_update(ann,H11,H1n,IN1,INn,gamma);    // in -> h1
}

void write_weights_to_file(ann_t *ann, int i1, int in, int j1, int jn, FILE *f_weights) {	// output/input block from-to
    for(int i=i1; i<=in; i++) {
		fprintf(f_weights, "%.8f\n", w(i,0));
        for(int j=j1; j<=jn; j++) {
			fprintf(f_weights, "%.8f\n", w(i,j));
        }
    }
}

// ----------------------------------------------------------------------------- MAIN
int main(void) {
    ann_t *ann=(ann_t*)malloc(sizeof(ann_t));
    FILE *f_images, *f_joints, *f_weights;  // file inputs/output
    char image_line[100000], joint_line[100];   // one line from image/joint file
    char *rgb_str;  // rgb value as string
    double rgb_value;   // rgb value as number
    double joint1, joint2;  // joint values
    struct timeb t; ftime(&t); srand(42);//srand(t.time);   // time-seed random generator

    MLP2_rnd_init(ann,-0.1,0.1);    // initialize the network

    for(int e=0; e<=Epochs; e++) {  // for every epoch
        double err1=0.0, err2=0.0;  // total errors in one epoch
		int data = 0;	// number of input data files
        f_images=fopen("images.txt", "r");
        f_joints=fopen("joints.txt", "r");

        if(f_images == NULL || f_joints == NULL) {
            printf("ERROR: Files images.txt or joints.txt did not open correctly");
            return(1);
        }
		
		
        while(fgets(image_line, 100000, f_images) != NULL) {    // read every image until end of file
			fgets(joint_line, 100, f_joints);   // also read joints for that image

            int input_index=IN1;
            rgb_str=strtok(image_line, " ");    // read first rgb value
            while(rgb_str != NULL) {
                sscanf(rgb_str, "%lf", &rgb_value);
                y(input_index)=rgb_value;   // save rgb value
                input_index++;
                rgb_str=strtok(NULL, " ");  // read rgb values until string comes to an end
            }

            sscanf(joint_line, "%lf %lf", &joint1, &joint2);    // read joint values for read image
            dv(OU1)=joint1; dv(OU2)=joint2; // store joint values as desired output

            MLP2_vanilla_bp(ann,Gamma); // train
            MLP2_run(ann);  // run network

            double J1=fabs(dv(OU1) - y(OU1));   // compute the error
            double J2=fabs(dv(OU2) - y(OU2));
            err1 += J1;
            err2 += J2;
			data++;
			
			if(e%100==0) {										// every 100 ep. print error
				printf("%5d: %f %f (%.6f) %f %f (%.6f)\n",e,y(OU1),dv(OU1),J1,y(OU2),dv(OU2),J2);
			}
        }
        
        fclose(f_images);
        fclose(f_joints);

        if ((err1 / data < 0.005) && (err2 / data < 0.005)) {
            printf("%d: %f %f\n", e, err1 / data, err2 / data);
            break;
        }
    }
	
    f_weights=fopen("weights.txt", "w");
    write_weights_to_file(ann,H11,H1n,IN1,INn,f_weights);	// in -> h1
    write_weights_to_file(ann,OU1,OUn,H11,H1n,f_weights);	// h1 -> ou
    fclose(f_weights);
	
    free(ann);

    return(0);
}

// ------------------------------------------------------------------------------ END
