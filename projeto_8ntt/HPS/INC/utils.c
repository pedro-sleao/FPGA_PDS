#include <stdio.h>
#include <stdint.h>
#include <string.h>

/*
* Separa uma string em N inteiros de acordo com o group_size
*/
void split_str_to_ints16(char *buf, int N, int group_size, int16_t *out) {
    for (int i = 0; i < N; i++) {
            char temp[4 + 1];
            strncpy(temp, &buf[i * group_size], group_size);
            temp[group_size] = '\0';
            sscanf(temp, "%d", &out[i]);
    }
}

/*
* Converte um array de N inteiros em uma string onde cada número ocupa exatamente group_size caracteres
*/
void ints16_to_str_fixed_width(int16_t *array, int N, int group_size, char *out_buf) {
    char format[8];
    snprintf(format, sizeof(format), "%%0%dd", group_size);

    for (int i = 0; i < N; i++) {
        char temp[group_size + 1];
        snprintf(temp, sizeof(temp), format, array[i]);
        strncpy(&out_buf[i * group_size], temp, group_size);
    }

    out_buf[N * group_size] = '\0';
}