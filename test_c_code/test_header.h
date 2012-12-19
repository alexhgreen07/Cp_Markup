#ifndef _test_header_h_
#define _test_header_h_

struct Opaque_Struct;

struct Public_Struct
{
	int public_var1;
	char public_var2;
	struct Opaque_Struct * private_data;
};


extern const int Opaque_Struct_sizeof;

#endif
