#ifndef __NTT_H__
#define __NTT_H__

#include <stdint.h>

#define N 8
#define Q 3329
#define N_INV 2497

static const int16_t ZETA[4] = {1, 1600, 40, 749};
static const int16_t ZETA_MULT[4] = {40, 3289, 749, 2580};

void ct_ntt_8_3329(int16_t *f);

void gs_intt_8_3329(int16_t *f);

void multiply_ntt(const int16_t *f, const int16_t *g, int16_t *h);

#endif