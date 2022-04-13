#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/sha.h>

#define TOC_MAX_LEN    (2 + 100)

int main(int argc, char **argv)
{
    char buf[2*2 + 100*8 + 1] = "";
    unsigned int toc[TOC_MAX_LEN] = {0};

    // calc-discid <first_track> <last_track> <lead_out> <offset_1> [offsets ...]
    if(argc < 1 + 2 + 2) {
        puts("ERROR: too few arguments");
        return 1;
    }
    // XXX: beware of too many offsets

    for(int i=1; i < argc; i++) {
        toc[i-1] = atoi(argv[i]);
        if(toc[i-1] == 0) {
            puts("ERROR: invalid track number or offset");
            return 1;
        }
    }

    if(snprintf(buf, 3, "%02X", toc[0]) > 2) {
            puts("ERROR: invalid track number or offset");
            return 1;
    }
    if(snprintf(buf+strlen(buf), 3, "%02X", toc[1]) > 2) {
            puts("ERROR: invalid track number or offset");
            return 1;
    }

    for(int i=2; i<TOC_MAX_LEN; i++) {
        if(snprintf(buf+strlen(buf), 9, "%08X", toc[i]) > 8) {
            puts("ERROR: invalid track number or offset");
            return 1;
        }
    }

    unsigned char hash[SHA_DIGEST_LENGTH]; // == 20
    SHA1((unsigned char*) buf, strlen(buf), hash);
    printf("%s\n", hash);

    return 0;
}
