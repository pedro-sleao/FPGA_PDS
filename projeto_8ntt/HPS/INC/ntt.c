#include <stdio.h>
#include <stdint.h>
#include <math.h>

#include "ntt.h"


void mul_test(const int16_t *a, const int16_t *b, int16_t *c) {
    int mask = N - 1;

    for (int i = 0; i < N; ++i) c[i] = 0;

    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            int index = (i + j) & mask;
            int32_t prod = (int32_t)a[i] * b[j];

            if (i + j >= N) {
                c[index] = (c[index] - prod + Q) % Q;
            } else {
                c[index] = (c[index] + prod) % Q;
            }
        }
    }
}

void ct_ntt_8_3329(int16_t *f) {
    int i = 1;
    for (int len = N/2; len >= 2; len /= 2) {
        for (int start = 0; start < N; start += 2*len) {
            int16_t zeta = ZETA[i++];
            for (int j = start; j < start + len; j++) {
                int16_t t = zeta*f[j+len] % Q;
                f[j+len] = (f[j] - t + Q) % Q;
                f[j] = (f[j] + t) % Q;
            }
        }
    }
}

void gs_intt_8_3329(int16_t *f) {
    int i = (N / 2) - 1;
    for (int length = 2; length <= N / 2; length *= 2) {
        for (int start = 0; start < N; start += 2 * length) {
            int16_t zeta = ZETA[i--];
            for (int j = start; j < start + length; j++) {
                int16_t t = f[j];
                f[j] = (f[j + length] + t) % Q;
                f[j + length] = (zeta * (f[j + length] - t + Q)) % Q;
            }
        }
    }

    for (int i = 0; i < N; ++i) {
        f[i] = (f[i] * N_INV) % Q;
    }
}

static void base_case_multiply(int16_t a0, int16_t a1, int16_t b0, int16_t b1, int16_t gamma, int16_t *c0, int16_t *c1) {
    *c0 = ((int32_t)a0 * b0 + ((int32_t)a1 * b1 % Q) * gamma) % Q;
    *c1 = ((int32_t)a0 * b1 + (int32_t)a1 * b0) % Q;
}

void multiply_ntt(const int16_t *f, const int16_t *g, int16_t *h) {
    for (int i = 0; i < N / 2; ++i) {
        base_case_multiply(f[2*i], f[2*i + 1], g[2*i], g[2*i + 1], ZETA_MULT[i], &h[2*i], &h[2*i + 1]);
    }
}
