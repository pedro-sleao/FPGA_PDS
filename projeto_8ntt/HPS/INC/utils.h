#ifndef __UTILS_H__
#define __UTILS_H__

#include <stdint.h>

void split_str_to_ints16(char *buf, int N, int group_size, int16_t *out);

void ints16_to_str_fixed_width(int16_t *array, int N, int group_size, char *out_buf);

#endif