#include <stdio.h>
#include "test_header.h"


int main(void)
{
	
	printf("The size of the opaque structure is '%d'.\n\n",Opaque_Struct_sizeof);
	printf("The size of the public structure is '%d'.\n\n",sizeof(struct Public_Struct));
	
}
