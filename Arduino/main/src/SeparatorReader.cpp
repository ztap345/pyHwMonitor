#include "SeparatorReader.h"

SeparatorReader::SeparatorReader(Stream *serial)
{
    serialPtr = serial;
    Reset();
}

// use a pointer to switch between the id and value buffers
// switch when we see 'KEY_VAL_SEPARATOR'. This lets use get Strings like "id:value"
// also listens for the stop code "*\n" which will cleanup and start waiting
void SeparatorReader::Read(){
    if(serialPtr->available() > 0 && !stopped && !readReady()){
        last_read = serialPtr->read();

        // set buffer pointer to the id buffer;
        if(!buffPtr){
            buffPtr = &keyBuff;
        }

        if(last_read == KEY_VAL_SEPARATOR){
            // if separator char was found then switch buffers
            buffPtr = &valueBuff;
            separatorFound = true;
        }else if(last_read != NEWLINE){
            // add if newline not read
            *buffPtr += last_read;
        }else{
            // newline was read, clear buffer is early stop or separator wasn't found
            if(!separatorFound){
                if((keyBuff.length()==1 && keyBuff[0] == STOP_CHAR)){
                    stopped = true;
                    Serial.println("STOPPED");
                }
                ClearBuffers();
            }
        }
    }

    if((millis() - ready_millis) > READY_TIMEOUT){
        Serial.println("TIMEDOUT");
        stopped = true;
    }
}

bool SeparatorReader::readReady(){
    return separatorFound && last_read == NEWLINE;
}

bool SeparatorReader::isStopped(){
    return stopped;
}

void SeparatorReader::Reset(){
    ClearBuffers();
    separatorFound = false;
    stopped = false;
    ready_millis = millis();
}

void SeparatorReader::ClearBuffers(){
    keyBuff = "";
    valueBuff = "";
    last_read = ' ';
    buffPtr = NULL;
}

String SeparatorReader::GetKey(){
    return keyBuff;
}

String SeparatorReader::GetValue(){
    return valueBuff;
}
