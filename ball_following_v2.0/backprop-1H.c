/* Backprop I: The Chosen One  */
/* autor: Denis Vereš          */
/* email: sinedko@gmail.com    */
/* year: 2015                  */

/*  Basic includes   */
#include <stdio.h>   // printf
#include <stdlib.h>  // rand, srand
#include <math.h>    // exp, abs
#include <time.h>    // clock

/* Definition of neural network */
#define IN 2304                    // number of input neurons
#define H1 3                   // number of neurons in first hidden layer
#define OUT 2                   // number of output neurons
#define N (1+IN+OUT+H1)         // number of total neurons

/*      Numbers of neurons      */
#define F1H 1+IN                // no. of first neuron in first hidden layer
#define L1H F1H+H1-1            // no. of last neuron in first hidden layer
#define FO F1H+H1               // no. of first neuron in output layer
#define LO FO+OUT-1             // no. of last neuron in output layer

/* Definition of learning */
#define gamma 0.2         // learning rate
#define epochs 10000      // number of learning epochs
#define tPoints 2000      // number of training points

/*             Activation function and its first derivation             */
#define f(x) (1.0/(1.0+exp((-1.0)*x)))                                  // sigmoidal activation function
#define df(x) (exp((-1.0)*x)/((1.0+exp((-1.0)*x))*(1.0+exp((-1.0)*x)))) // derivation of sigmoidal function

/* Structure of neural network */
typedef struct nn {            // --------------------
    double x[N];               // inputs in neurons
    double y[N];               // activations of inputs
    double d[N];               // error signal (difference)
    double w[N][N];            // weights matrix
    double dv[OUT];            // desired value on output
} NN;

NN network = {}; // declaration of neural network

/*   Some useful definitions   */
#define x(i) network.x[i]      // inputs
#define y(i) network.y[i]      // activations
#define d(i) network.d[i]      // deltas
#define w(i,j) network.w[i][j] // weights
#define dv(i) network.dv[i]    // desired outputs

/*      Function for passing individual layers    */
void layerRun(int from[], int to[]) {             // --------------------
    for (int j = from[0]; j < to[0]; j++) {       // from first neuron in specific layer to last
        //printf("\nx(%d) = w(0,%d) * y(0) + ",j,j);// --------------------
        x(j) = w(0,j) * y(0);                     // adding bias to the sum
        for (int i = from[1]; i <= to[1]; i++) {  // from first neuron to last neuron specific layer
            x(j) += w(i,j) * y(i);                // using formula to compute neuron input
            //printf("w(%d)(%d) * y(%d) + ",i,j,i); // --------------------
        }                                         // --------------------
        y(j) = f(x(j));                           // using activation function with neuron inputs to gain activations
    }
    //printf("\n---------");
}

/* Function for passing over the network (forward pass) */
void forwardRun() {
    int from[2], to[2]; // declarations of auxiliary arrays
    
    /* Going through first hidden layer  */
    from[0] = F1H; to[0] = L1H + 1;      // definitions from-to for j (from first to last in first hidden layer)
    from[1] =   1; to[1] = IN;           // definitions from-to for i (from first to last in input layer)
    layerRun(from,to);                   // runs function
    
    /*     Going through output layer    */
    from[0] =  FO; to[0] = LO + 1;       // definitions from-to for j (from first to last in output layer)
    from[1] = F1H; to[1] = L1H;          // definitions from-to for i (from first to last in second hidden layer)
    layerRun(from,to);                   // runs function
}

FILE * fp, * fin ;

void loadWeights(int from[], int to[], int fix) {
    for (int j = from[0]; j <= to[0]; j++) {
        if (fix==1) fscanf(fp,"%lf",&w(0,j));
        for (int i = from[1]; i < to[1]; i++) fscanf(fp,"%lf",&w(i,j));
    }
}

void loadHelper() {
    int from[2],to[2];

    from[0] =   F1H;  to[0] = L1H;
    from[1] = 0; to[1]  = F1H;
    loadWeights(from,to,0);

    from[0] =   FO;  to[0] = LO;
    from[1] = F1H; to[1]  = L1H+1;
    loadWeights(from,to,1);
}

int main () {
    fp = fopen ("weights.txt","r");
    fin = fopen("image.txt","r");

    loadHelper();
    fclose(fp);

    y(0) = -1;
    for (int i = 1; i <= IN; i++) fscanf(fin,"%lf",&y(i));

    fclose(fin);

    forwardRun();                           // train

    printf("%f %f",y(FO),y(LO));
    return 0;
}