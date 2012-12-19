#include "test_header.h"

struct Opaque_Struct
{
	int test_data1;
	char bufer[20];
};

const int Opaque_Struct_sizeof = sizeof(struct Opaque_Struct);
