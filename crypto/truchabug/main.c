#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <tomcrypt.h>
#include <gmp.h>

#define SHA256_SIZE 32

char* PKEY_N = "28316605750203454049002363560313563954296751450828848448517208195421674434602842807549596897970975529201316850622185623315583333237800231329023940484748688010961986901515147691858248996029931794630763468134269876901486229211372065501121751105623386156595213445891671288794107312313963247118259644196378662929869385025707884211817553083248681280118820740363347221337328761267079917222413767989397087611382611167569151505277047991858303445030096445782329982462564958470982918402018945533966426750370205997840705200810347367312283800916365954203381180315167389062039395265242886707651891538103937713233762440148808375849";
unsigned long PKEY_E = 65537;

bool check_signature(unsigned char* content, int content_len, mpz_t signature) {
    hash_state md;
    sha256_init(&md);

    unsigned char computed_hash[SHA256_SIZE];
    sha256_process(&md, content, content_len);
    sha256_done(&md, computed_hash);

    char computed_hash_str[SHA256_SIZE * 2 + 1]; // don't forget the + 1 for the null byte

    for (int i = 0; i < SHA256_SIZE; i++) {
        sprintf(&computed_hash_str[i * 2], "%02x", computed_hash[i]);
    }

    mpz_t computed_hash_mpz;
    mpz_init(computed_hash_mpz);
    mpz_set_str(computed_hash_mpz, computed_hash_str, 16);

    mpz_t n;
    mpz_init(n);
    mpz_set_str(n, PKEY_N, 10);

    // the + 5 and + 4 in the following piece of code are because mpz_out_raw exports not just the raw bytes of the number, but a specific sequence consisting of :
    // - 4 bytes of size information, containing the size in bytes of the number
    // - the bytes of the number itself
    // - 1 ending null byte
    unsigned char in_mem_buf[SHA256_SIZE + 5];
    unsigned char decrypted_hash[SHA256_SIZE];

    mpz_t dec_sig;
    mpz_init(dec_sig);
    mpz_powm_ui(dec_sig, signature, PKEY_E, n);

    FILE* in_mem_buf_f = fmemopen(in_mem_buf, SHA256_SIZE + 5, "w");
    mpz_out_raw(in_mem_buf_f, dec_sig);
    fclose(in_mem_buf_f);

    memcpy(decrypted_hash, in_mem_buf + 4, SHA256_SIZE);

    mpz_clear(computed_hash_mpz);
    mpz_clear(n);
    mpz_clear(dec_sig);

    return strncmp(computed_hash, decrypted_hash, SHA256_SIZE) == 0;
}

void remove_trailing_line_feed(char* str) {
    str[strcspn(str, "\n")] = 0;
}

int main(void) {
    printf("What do you want? Please select one of these:\n");
    printf("- the date\n");
    printf("- the flag\n");
    printf("- the answer to life, the universe and everything\n");
    fflush(stdout);

    int input_size = 100;
    char input[input_size];

    fgets(input, input_size, stdin);
    remove_trailing_line_feed(input);

    if (strstr(input, "flag") != NULL) {
        printf("Okay, but before that I need you to prove me I can trust you... Please send me now the raw RSA signature of what you just sent, as a base 10 number.\n");
        fflush(stdout);

        char signature_str[1000];
        fgets(signature_str, 1000, stdin);
        remove_trailing_line_feed(signature_str);

        mpz_t signature;
        mpz_init(signature);
        int failure = mpz_set_str(signature, signature_str, 10);
        if (failure) {
            printf("That's not a base 10 number.\n");
            fflush(stdout);
            return 1;
        }

        if (check_signature(input, strlen(input), signature)) {
            FILE* f = fopen("flag.txt", "r");
            int flag_size = 100;
            char flag[flag_size];
            fgets(flag, flag_size, f);

            printf("Sure, here is the flag: %s\n", flag);
            fflush(stdout);
        }
        else {
            printf("Who are you!? This is a secret! Stop it!\n");
            fflush(stdout);
        }

        mpz_clear(signature);
    }
    else if (strstr(input, "date") != NULL) {
        FILE* fp = popen("date", "r");
        int date_size = 100;
        char date[date_size];
        fgets(date, date_size, fp);
        pclose(fp);

        printf("The date is %s\n", date);
        fflush(stdout);
    }
    else if (strstr(input, "answer") != NULL) {
        printf("The answer is 23 (if you expected 42, you were wrong)\n");
        fflush(stdout);
    }
    else {
        printf("Sorry but I didn't understand\n");
        fflush(stdout);
    }

    return 0;
}