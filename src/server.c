// Vorlage Vorlesung

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <signal.h>

int f;

void signal_handler(int sig)
{
    fprintf(stderr, "graceful shutdown requested: %d\n", sig);
    shutdown(f, SHUT_RDWR);
    exit(0);
    return;
}

int main(int argc, char **argv)
{
    f = socket(PF_INET, SOCK_STREAM, 6);
    if (f == -1) {
        perror("socket");
        return 1;
    }

    signal(2, signal_handler);
    signal(15, signal_handler);

    struct sockaddr_in address;
    memset(&address, 0, sizeof(struct sockaddr_in));
    address.sin_family = AF_INET;
    address.sin_port = htons(8080);

    int r = bind(f, (const struct sockaddr *) &address, sizeof(struct sockaddr_in));
    if (r != 0) {
        perror("bind failed");
        return 2;
    }

    do {
        r = listen(f, 10);
    } while (r != 0 && errno == EINTR);
    if (r != 0) {
        perror("listen failed");
        return 3;
    }

    struct sockaddr_in client;
    socklen_t client_size = sizeof(struct sockaddr_in);

    pid_t p = 0;
    do {
        int cf = 0;
        do {
            cf = accept(f, (struct sockaddr *) &client, &client_size);
        } while (cf == -1 && errno == EINTR);
        if (cf == -1) {
            perror("accept failed");
            return 4;
        }

        p = fork();
        if (p == 0) {
            // I am the child process
            setuid(501);
            const size_t MAX_BUF_SIZE = 1024;
            char buffer[MAX_BUF_SIZE];

            do {
                ssize_t c = 0;
                do {
                    c = recv(cf, buffer, MAX_BUF_SIZE, 0);
                } while (c < 0 && errno == EINTR);
                if (c < 0) {
                    perror("error reading data");
                    // wait for next input
                }
                if (c >= 3 && strncmp(buffer, "end", 3) == 0) {
                    shutdown(cf, SHUT_RDWR);
                    break;
                }

                if (c >= 5 && strncmp(buffer, "hello", 5) == 0) {
                    memcpy(buffer, "world", 5);
                    ssize_t c2 = 0;
                    do {
                        c2 = send(cf, buffer, 5, 0);
                    } while (c2 < 0 && errno == EINTR);
                }
            } while (1);
            break;
        }
        else {
            // I am the parent process
            continue;
        }
    } while (1);

    if (p != 0) {
        shutdown(f, SHUT_RDWR);
        close(f);
    }

    return 0;
}
