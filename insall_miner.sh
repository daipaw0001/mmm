git clone https://github.com/OhGodAPet/cpuminer-multi.git;cd cpuminer-multi; sudo apt-get update ; sudo apt-get install -y screen automake build-essential autoconf pkg-config libcurl4-openssl-dev libjansson-dev libssl-dev libgmp-dev libncurses5-dev tmux yasm; ./autogen.sh ; CFLAGS="-march=native" ./configure --disable-aes-ni ; make ; tmux new-session -d "./minerd -a cryptonight -o stratum+tcp://mro.pool.minergate.com:45560 -u caoazerty01@gmail.com -p x"