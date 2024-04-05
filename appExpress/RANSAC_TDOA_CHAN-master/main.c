#include <stdio.h>
#include <math.h>
#include <time.h>

#include "ransac_tdoa.h"
// #include "ransac_tdoa_gsl.h"

double* tdoa_cal(double lmx[],double lmy[],int TEST_LANDMARK_NUM,double difference_of_distances[]) {
    Position2D landmarks[TEST_LANDMARK_NUM];
    for(int i=0;i<TEST_LANDMARK_NUM;i++){
    	landmarks[i].x =lmx[i];  
    	landmarks[i].y =lmy[i];
    }   
    //double difference_of_distances[TEST_LANDMARK_NUM]; // difference of distance comparing with landmark 0
    //difference_of_distances[0] = 0;
    double std_dev = 0.01;
  
    double estimated_x, estimated_y;
    int effective_landmark_mask[TEST_LANDMARK_NUM];
    for (int i = 0; i < TEST_LANDMARK_NUM; i++) {
        effective_landmark_mask[i] = 1;
    }
    // effective_landmark_mask[2] = 0; // uncomment this line to test that 'effective_landmark_mask' works
    clock_t start, finish;
    Position2D pos;
    start = clock();
    int success = tdoa_ransac(landmarks, difference_of_distances, effective_landmark_mask, TEST_LANDMARK_NUM, std_dev,
        &pos);
    finish = clock();
    double *ans=malloc(2 * sizeof(double));
    ans[0]=pos.x;
    ans[1]=pos.y;
    
    return ans;
}
int main(){
    return 0;
}
