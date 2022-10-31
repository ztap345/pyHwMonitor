#ifndef MESSAGE_RECEIVER_H
#define MESSAGE_RECEIVER_H

#include "ConfigConstants.h"
#include "SeparatorHandler.h"

class MessageReceiver
{
private:
    String lineBuffer;
    bool startFound;
    String startString;
    String endString;

public:
    MessageReceiver(String startString, String endString);
    ~MessageReceiver();
    void readChar(char c, SeparatorHandler* m);
    bool isFinished();
    void clear();
};

MessageReceiver::MessageReceiver(String start, String end)
{
    startString = start;
    endString = end;
    clear();
}

MessageReceiver::~MessageReceiver()
{
    clear();
}

void MessageReceiver::readChar(char c, SeparatorHandler* m){
    if(c != NEWLINE){
        lineBuffer += c;
    }else{
        if(lineBuffer == startString){
            startFound = true;
            lineBuffer = "";
        }else if(startFound && lineBuffer != endString){
            m->handleMsg(lineBuffer);
            lineBuffer = "";
        }else if(!startFound){
            lineBuffer == "";
        }
    }

}

bool MessageReceiver::isFinished(){
    return lineBuffer == endString;
}

void MessageReceiver::clear(){
    startFound = false;
    lineBuffer = "";
}


#endif