import "OS.cp";

using stdio;
using OS::Memory;

namespace OS
{
    //class definition using stack based parameters
    class String(unsigned int buffer_length)
    {
        //this will be a pointer when initialized dynamically, an array when initialized statically
        public char raw_buffer[buffer_length];
        //the buffer total size
        public unsigned int buffer_size = buffer_length;
        //the current string length
        public unsigned int string_length = 0;
        
        //heap allocator
        public static String * New(unsigned int buffer_length)
        {
            String * return_handle;
            
            //allocate memory using sizeof string
            return_handle = OS::Memory::malloc(sizeof(String));
            
            return_handle->raw_buffer = OS::Memory::malloc(buffer_length);
            
            return_handle->buffer_size = buffer_length;
            
            return_handle->string_length = 0;
            
            return return_handle;
        }
        
        //heap free
        public void Free(void)
        {
            //free the raw buffer
            OS::Memory::free(this->raw_buffer);
            
            //free the actual object
            OS::Memory::free(this);
            
        }
        
        //copy function
        public void Copy(String * destination)
        {
            //copy main class data (ptr_src, ptr_dest, size)
            OS::Memory::copy(this->raw_buffer, destination->raw_buffer, this->string_length);
            
            destination->string_length = this->string_length;
            
        }
    }
}
