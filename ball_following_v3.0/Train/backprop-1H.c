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
#define IN 2304+2304            // number of input neurons
#define H1 16*12                // number of neurons in first hidden layer
#define OUT 2                   // number of output neurons
#define N (1+IN+OUT+H1)         // number of total neurons

/*      Numbers of neurons      */
#define F1H 1+IN                // no. of first neuron in first hidden layer
#define L1H F1H+H1-1            // no. of last neuron in first hidden layer
#define FO F1H+H1               // no. of first neuron in output layer
#define LO FO+OUT-1             // no. of last neuron in output layer

/* Definition of learning */
#define gamma 0.2         // learning rate
#define epochs 15000      // number of learning epochs

/*             Activation function and its first derivation             */
#define f(x) (1.0/(1.0+exp((-1.0)*x)))                                  // sigmoidal activation function
#define df(x) (exp((-1.0)*x)/((1.0+exp((-1.0)*x))*(1.0+exp((-1.0)*x)))) // derivation of sigmoidal function

#define inputCode(x) ((2 * x) / 255) - 1
#define inputDecode(x) ((255 * x) + 255) / 2
#define outputCode(x) (x + 4.1714) / 8.3428
#define outputDecode(x) (x * 8.3428) - 4.1714

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

/* Function for initialize random weights in interval <min,max> */
void initWeights(double min, double max) {                      // --------------------
    y(0) = -1;                                                  // initialize the input of bias
                                                                // --------------------
    for (int i = 0; i < N; i++)                                 // go through array
        for (int j = 0; j < N; j++)                             // same
            w(i,j) = rand() / (RAND_MAX/(max-min)) + min;       // sets random number to the array
}

/*      Function for passing individual layers    */
void layerRun(int from[], int to[]) {             // --------------------
    for (int j = from[0]; j < to[0]; j++) {       // from first neuron in specific layer to last
        //printf("\nx(%d) = w(0,%d) * y(0) + ",j,j);// --------------------
        x(j) = w(0,j) * y(0);                     // adding bias to the sum
        for (int i = from[1]; i <= to[1]; i++) {  // from first neuron to last neuron specific layer
            x(j) += w(i,j) * y(i);                // using formula to compute neuron inputs
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

/* Function for passing over a network to compute deltas */
void deltaRun(int from[], int to[]) {                    // --------------------
    for (int i = from[0]; i <= to[0]; i++) {             // from first neuron in specific layer to last
        d(i) = 0;                                        // clear old delta
        //printf("\nd(%d) = ",i);                        // --------------------
        for (int j = from[1]; j <= to[1]; j++) {         // from first neuron in specific layer to last
            //printf("d(%d) * w(%d)(%d) + ",j,i,j);      // --------------------
            d(i) += d(j) * w(i,j);                       // using formula to compute delta
        }                                                // --------------------
        d(i) *= df(x(i));                                // multiply with first derivation of activation function
    }
}

/* Function for passing over the network (backward pass) */
void backwardRun() {
    int from[2],to[2]; // declarations of auxiliary arrays
    
    /*      Compute deltas in output layers      */
    for (int i = FO, j = 0; i <= LO; i++, j++) { // from first to last neuron in output layer
        d(i) = (dv(j) - y(i)) * df(x(i));        // using formula to compute deltas on output layer
        //printf("\nd(%d) = (dv(%d) - y(%d)) * df(x(%d))",i,j,i,i);
    }
    //printf("\n---------");
    
    /* Compute deltas in first hidden layer  */
    from[0] = F1H; to[0] = L1H;              // definitions from-to for j (from first to last in first hidden layer)
    from[1] =  FO; to[1] =  LO;              // definitions from-to for i (from first to last in second hidden layer)
    deltaRun(from,to);                       // runs function
}

/* Function for passing over the network and update weights */
void weightsRun(int from[], int to[]) {                     // --------------------
    for (int i = from[0]; i <= to[0]; i++)                  // from first neuron in specific layer to last
        for (int j = from[1]; j<= to[1]; j++) {             // same
            w(i,j) += (d(j) * y(i) * gamma);                // using formula for updating weights
            //printf("\nw(%d)(%d) += d(%d) * y(%d) * gamma",i,j,j,i);
        }
}

/* Function for passing over the network (updating weights) */
void weightsUpdate() {
    int from[2], to[2]; // declarations of auxiliary arrays
    
    /*    Changing weights for bias     */
    from[0] =   0;  to[0] =  0;         // --------------------
    from[1] = F1H; to[1]  = LO;         // definitions from-to for i (from first to last neuron in network)
    weightsRun(from,to);                // runs function
    
    /* Changing weights for input layer */
    from[0] =   1; to[0] =  IN;         // definitions from-to for j (from first to last in input layer)
    from[1] = F1H; to[1] = L1H;         // definitions from-to for i (from first to last in first hidden layer)
    weightsRun(from,to);                // runs function
    
    /* Going through first hidden layer */
    from[0] = F1H; to[0] = L1H;         // definitions from-to for j (from first to last in first hidden layer)
    from[1] =  FO; to[1] =  LO;         // definitions from-to for i (from first to last in second hidden layer)
    weightsRun(from,to);                // runs function
}

void weightsToFile(int from[], int to[], int fix, FILE * weights) {   // output/input block from-to
    for (int j = from[0]; j <= to[0]; j++) {
        if (fix==1) fprintf(weights,"%.8f\n",w(0,j));
        for (int i = from[1]; i < to[1]; i++) fprintf(weights,"%.8f\n",w(i,j));
    }
}

void weightsToFileHelper() {
    int from[2], to[2]; // declarations of auxiliary arrays
    FILE *weights = fopen("weights.txt","w");
    
    from[0] =   F1H;  to[0] = L1H;
    from[1] = 0; to[1]  = F1H;        
    weightsToFile(from,to,0,weights); 
    
   
    from[0] =   FO;  to[0] = LO;
    from[1] = F1H; to[1]  = L1H + 1;        
    weightsToFile(from,to,1,weights);

    fclose(weights);
}

int main () {
    //int XOR[4][3] = {{0,0,0,},{0,1,1,},{1,0,1,},{1,1,0,}};	// XOR data
    clock_t t;             // auxiliary variable for compute running time
    float sec;             // auxiliary variable for compute seconds
    double error1,error2;
    int sumData = 0, tPoints = 0;
    char trash[50000];
                           // --------------------
    srand(time(NULL));             // seed for random numbers
    initWeights(-0.1,0.1); // initialize weights
    FILE * trainingSet = fopen("trainingData.txt","r");
    FILE * con1 = fopen("con1.txt","w");
    FILE * con2 = fopen("con2.txt","w");
    while (fgets (trash, 50000 , trainingSet) != NULL) tPoints++;
    t = clock();           // start timer
    
    //printf("\nEpoch:  Output  Des.out. (Error)\n"); // --------------------
    //printf("--------------------------------\n");   // --------------------
    int epoch;                                        // --------------------
    for (epoch = 0; epoch <= epochs; epoch++) { // for every 
        error1 = 0, error2 = 0;
        rewind(trainingSet);
        
        for (int p = 0; p < tPoints; p++) {			// for every pattern
            
            for (int img = 1; img <= IN; img++) {
                fscanf(trainingSet,"%lf",&y(img));
                y(img) = inputCode(y(img));
            }
            fscanf(trainingSet,"%lf %lf",&dv(0),&dv(1));
            dv(0) = outputCode(dv(0));
            dv(1) = outputCode(dv(1));
                                                    // --------------------
            forwardRun();                           // train
            backwardRun();                          // train
            weightsUpdate();                        // train

            double J1=fabs(dv(0) - y(FO));      // compute the error
            double J2=fabs(dv(1) - y(LO));      // compute the error

            error1 += J1;
            error2 += J2;
            sumData++;
                                                    // --------------------
            if (epoch % 100==0) {				    // every 20000 ep. print error
                if (p == 0 && epoch != 0) {
                    printf("\n");
                    printf("\n%f %f\n",error1,error2);
                }          // --------------------
                    		            // --------------------
                //forwardRun();                       // runs network
                //if (p % 20 == 0) 
                printf("%5d: %f %f (%.6f) ::: %f %f (%.6f)\n",epoch,y(FO),dv(0),J1,y(LO),dv(1),J2);
            }
        }

        fprintf(con1,"%f ",error1 / tPoints);
        fprintf(con2,"%f ",error2 / tPoints);

        if ((error1 / tPoints < 0.005) && (error2 / tPoints < 0.005)) {
            printf("%5d: %f %f\n", epoch, error1 / sumData, error2 / sumData);
            break;
        }
    }
    fprintf(con1,"\n%d ",epoch);
    fprintf(con2,"\n%d ",epoch);

    fclose(con1);
    fclose(con2);
    fclose(trainingSet);
    t = clock() - t;                 // stop timer
    sec = ((float)t)/CLOCKS_PER_SEC; // conversion to seconds
    
    //printf("--------------------------------\n%.3f sec\n\n",sec);
    weightsToFileHelper();
    //printf("%.3f ",sec);
    printf("%d",tPoints);
    return 0;
}