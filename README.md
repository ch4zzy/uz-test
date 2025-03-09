### Розгортання проекту

Залежності:
- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Makefile](https://www.gnu.org/software/make/)

1. Клонування репозиторію:
    ```sh
    git clone https://github.com/ch4zzy/uz-test
    ```
2. Перехід у директорію проекту:
    ```sh
    cd uz-test
    ```
   
3. Білд та запуск проекту:
    ```sh
    make
    ```
   
4. Заповнення бд тестовими даними:
    ```sh
    make fill-db
    ```
