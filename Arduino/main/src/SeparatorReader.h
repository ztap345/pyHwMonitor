#ifndef SEPARATOR_READER_H
#define SEPARATOR_READER_H

#include "ConfigConstants.h"
#include <string.h>
#include <Stream.h>
#include <wiring_private.h>

class SeparatorReader {
    private:
        Stream* serialPtr;
        char last_read;
        unsigned long ready_millis;

        String keyBuff;
        String valueBuff;
        String* buffPtr;
        boolean separatorFound;
        boolean stopped;

    public:
        SeparatorReader(Stream*);
        
        void Read();
        bool readReady();
        bool isStopped();
        void Reset();
        void ClearBuffers();
        String GetKey();
        String GetValue();
};

#endif