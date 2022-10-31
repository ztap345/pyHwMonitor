#ifndef SEPARATOR_HANDLER_H
#define SEPARATOR_HANDLER_H

#include <Vector.h>

class SeparatorHandler{
private:
    String* results = NULL;
    int stringCount;
    char separator;
    char endChar;
    int maxCount;
    void clear(){
        if(results != NULL){    
            delete [] results;
        }
        results = new String[maxCount];
    };

public:
    void init(char sep, char end, int max){
        separator = sep;
        endChar = end;
        maxCount = max;
        clear();
    }
    String* get(){return results;}
    int get_max(){return maxCount;}
    void handleMsg(String c);

};

void SeparatorHandler::handleMsg(String c){
    clear();
    stringCount = 0;

    while(c.length() > 0){

        int i = c.indexOf(separator);

        if(stringCount == maxCount){
            Serial.println("BREAK");
            break;
        }
        
        if(i == -1){
            results[stringCount++] = c;
            break;
        }else{
            String value = c.substring(0, i);
            results[stringCount++] = value;
            c = c.substring(i+1);
        }
    }
}

#endif