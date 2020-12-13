#ifndef CORE_H
#define CORE_H

// clips an integer at a value between 0 and 255. Values less than
// 0 will be set to 0, values larger than 255 will be set to 255.
#ifndef clip
#define clip(x) (x < 255 ? (x > 0 ? x : 0 ) : 255)
#endif

// finds the maximum of 2 values
#ifndef max
#define max(x,y) (x > y ? x : y)
#endif

// finds the minimum of 2 values
#ifndef min
#define min(x,y) (x < y ? x : y)
#endif

// a data type for a 3 channel pixel
typedef struct {
    unsigned char red;
    unsigned char green;
    unsigned char blue;
} pixel3;

// a data type for a 4 channel pixel
typedef struct {
    unsigned char red;
    unsigned char green;
    unsigned char blue;
    unsigned char alpha;
} pixel4;

#endif // CORE_H

