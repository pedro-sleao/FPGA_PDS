#include <stdio.h>
#include <stdint.h>
#include <math.h>

#define N 8
#define Q 3329
#define N_INV 2497

static const int16_t ZETA[4] = {1, 1600, 40, 749};
static const int16_t ZETA_MULT[4] = {40, 3289, 749, 2580};

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

void base_case_multiply(int16_t a0, int16_t a1, int16_t b0, int16_t b1, int16_t gamma, int16_t *c0, int16_t *c1) {
    *c0 = ((int32_t)a0 * b0 + ((int32_t)a1 * b1 % Q) * gamma) % Q;
    *c1 = ((int32_t)a0 * b1 + (int32_t)a1 * b0) % Q;
}

void multiply_ntt(const int16_t *f, const int16_t *g, int16_t *h) {
    for (int i = 0; i < N / 2; ++i) {
        base_case_multiply(f[2*i], f[2*i + 1], g[2*i], g[2*i + 1], ZETA_MULT[i], &h[2*i], &h[2*i + 1]);
    }
}

int main(void) {
    int16_t a[N] = {0, 1, 2, 3, 4, 5, 6, 7};
    int16_t b[N] = {0, 1, 2, 3, 4, 5, 6, 7};
    int16_t c[N], c_[N];

    mul_test(a, b, c_);
    for (int i = 0; i < N; i++) {
        printf("%d ", c_[i]);
    }
    printf("\n");
    
    ct_ntt_8_3329(a);
    ct_ntt_8_3329(b);

    multiply_ntt(a, b, c);

    gs_intt_8_3329(c);

    for (int i = 0; i < N; i++) {
        printf("%d ", c[i]);
    }
    printf("\n");

    return 0;
}