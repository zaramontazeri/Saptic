/* Start reading here */

#include <fftw3.h>

#define NUM_POINTS 65


/* Never mind this bit */

#include <stdio.h>
#include <math.h>

#define REAL 0
#define IMAG 1

void acquire_from_somewhere(fftw_complex* signal,fftw_complex* diff) {
    /* Generate two sine waves of different frequencies and
     * amplitudes.
     */
    int i;
    for (i = 0; i < NUM_POINTS; ++i) {
        double theta = (double)i / (double)NUM_POINTS * M_PI;

        signal[i][REAL] = 1.0 * cos(10.0 * theta) +
                          0.5 * cos(25.0 * theta);

        // signal[i][IMAG] = 1.0 * sin(10.0 * theta) +
        //                   0.5 * sin(25.0 * theta);
        signal[i][IMAG] = 0;
    }
    for (i = 0; i < NUM_POINTS-1; ++i) {
        diff[i][REAL] =signal[i+1][REAL]  - signal[i][REAL] ;
        // signal[i][IMAG] = 1.0 * sin(10.0 * theta) +
        //                   0.5 * sin(25.0 * theta);
        diff[i][IMAG] = 0;
    }

}

void do_something_with(fftw_complex* result) {
    int i;
    for (i = 0; i < NUM_POINTS; ++i) {
        double mag = sqrt(result[i][REAL] * result[i][REAL] +
                          result[i][IMAG] * result[i][IMAG]);

        printf("%g\n", mag);
    }
}


/* Resume reading here */

int main() {
    fftw_complex signal[NUM_POINTS];
    fftw_complex diff[NUM_POINTS];
    fftw_complex result[NUM_POINTS];

    fftw_plan plan = fftw_plan_dft_1d(NUM_POINTS,
                                      diff,
                                      result,
                                      FFTW_FORWARD,
                                      FFTW_ESTIMATE);

    acquire_from_somewhere(signal,diff);
    fftw_execute(plan);
    do_something_with(result);

    fftw_destroy_plan(plan);

    return 0;
}
