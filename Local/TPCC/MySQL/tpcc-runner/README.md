### TPC-C Benchmark on MySQL

The script in this repository will configure and run the TPC-C benchmark on MySQL.

The TPC-C implementation used is this one: https://github.com/pingcap/tpcc-mysql

That implementation is packaged in the following community-downloadable docker container: https://hub.docker.com/r/gaishimo/tpcc-mysql/

And MySQL is installed from the official MySQL community-downloadable container: https://hub.docker.com/_/mysql/

## Instructions

1. Install docker on your system, if not already installed:
`curl -sSL https://get.docker.com/ | sh`

2. Run the script in this repository:
```
wget https://raw.githubusercontent.com/ereyes01/tpcc-runner/master/tpcc.sh
chmod +x ./tpcc.sh
./tpcc.sh
```

The database and the TPC-C data will be loaded, which can take a while. When the test is started, the scrip will terminate and its output will tell you how to monitor the test and view the results.

The TPC-C test is executed with the following parameters:

- Warehouses: 4
- Connections: 8
- Ramp-up time: 1 minute
- Test time: 10 minutes
