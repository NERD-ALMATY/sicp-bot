# sicp-bot
Make SICP exercises great again

## Description
This project is intended to build a Telegram bot that can count the number of solved SICP exercises from github user repo.

## Getting Started

### Dependencies

* python3.7, requirements.txt, openssl
* docker, docker-compose

### Installation and Execution

* Clone the repo:
    ```
    git clone github.com/nerd-iitu/sicp-bot
    ```
* Copy and set your own `.env` properties:
    ```
    cp .env.sample .env
    # vim .env
    ```
* Generate the needed certificates and set the proper fields:
    ```
    cd data
    openssl genrsa -out key.pem 2048
    openssl req -new -x509 -days 3650 -key key.pem -out cert.pem
    cd ..
    ```
* Launch:
    ```
    docker-compose up -d
    ```

## TODO:

### Least Completable Minimum

* Write tests.
* Make it pythonic.
* Add CI/CD.
* Add docs

### More

* Optimize and rewrite the modules.
* Make the automatic code analysis and evaluation(scm, rkt fles) in order to proove the rightness of an answer
(would be easier to solve SICP tasks rather than writing another expression reducer).
* Solve SICP exercises :).

## FAQ or Help

Don't hesitate to create a new issue or dm me at [@arpanetus](t.me/arpanetus).


## Authors

Project maintainer:
    [@arpanetus](https://github.com/arpanetus)


## License

This project is licensed under the [NPOSL-3.0](LICENSE).
