# SQLvsNoSQLvsNewSQL

Installare Docker e scaricare la cartella dataset dal link https://drive.google.com/file/d/1j6fM2xW9z1MLb0AcG27luXT_trAakrbq/view?usp=sharing

Il progetto prevede di analizzare le performance di MySQL, MongoDB e CockroachDB. 
Quindi si è deciso di utilizzare Docker per containerizzare le tecnologie.
Si sono trovati tre casi d'uso per eseguire l'analisi delle performance.

**Primo caso d'uso.**

All'interno della cartella Local, si possono notare altre due cartelle Cluster e SingleNode, all'interno di queste cartelle 
ci sono i file Compose per ogni tecnologia ed il relativo main.py, quindi se si vuole testare ad esempio CockroachDB su un singolo nodo si
deve eseguire (dalla root del progetto) il comando : `docker-compose -f Local/SingleNode/CockroachDB/docker-compose.yaml up -d` quindi 
poi eseguire `python Local/SingleNode/CockroachDB/main.py 'host'` di default l'host è "localhost" oppure l'indirizzo IP scelto nel file relativo a Docker Compose.

All'interno della cartella relativa alla tecnologia scelta verranno creati i volumi necessari.

CockroachDB è l'unico che durante l'importazione del dataset necessita di un server di caricamento, quindi prima di eseguire 
il suo main, si deve eseguire un http server, ad esempio sempre dalla root del progetto eseguire il comando `python -m http.server`. 
I risultati sono visibili all'interno della cartella Result.
Per MySQL ci sono delle operazioni da fare per aggirare delle policy di sicurezza, si deve accedere alla bash del container quindi digitare `docker exec -it MySQL_SingleNode bash`, quindi accedere
alla console di MySQL digitando `mysql -u root -p`, digitare la password scritta nel file Compose, settare la variabile globale
local_infile a 1, digitare quindi `SET GLOBAL local_infile = 'ON';`. Così sarà possibile caricare i file csv.
Invece per MongoDB, basta eseguire il suo Compose ed il suo main.
Riguardo al cluster, si devono eseguire dei comandi prima di eseguire il main.

Per MongoDB, dopo aver eseguito docker-compose, eseguire i comandi presenti nel file "setup_mongodb_cluster.md".
Invece per CockroachDB, vi sono due implementazioni, un semplice cluster ed una multi-regione. In entrambi i casi
dopo aver eseguito docker-compose si deve eseguire una one-time initialization del cluster 
quindi eseguire `docker exec -it 'nome di un node del cluster' ./cockroach init --insecure`, quindi poi eseguire i relativi main
dalla root del progetto.

**Secondo caso d'uso.**

Innanzitutto si deve installare JMeter, https://jmeter.apache.org/download_jmeter.cgi

Quindi è possibile importare i file di configurazione prensenti in Local/JMeter_config, potrebbe essere necessario
cambiare gli indirizzi IP dei container, quindi se necessario eseguire `docker inspect 'nome container'` per sapere l'indirizzo ip di quel container comunque i risultati ottenuti sono presenti nella cartella Result_JMeter. Se necessario impostare server-proxy.

**Terzo caso d'uso.**

Spostarsi nella cartella Local/TPCC vi è una cartella per ogni tecnologia scegliere quindi la tecnologia dove eseguire 
il benchmark TPC-C e spostarsi all'interno di essa. 

Eseguire quindi il file Compose di Docker ed impostare server-proxy con indirizzo IP 172.28.0.5.

Per CockroachDB eseguire i seguenti comandi: 

Init cluster
`cockroach init --insecure --host=172.28.0.5:26257`

Import the TPC-C dataset
`cockroach workload fixtures import tpcc --warehouses=100 'postgresql://root@172.28.0.5:26257?sslmode=disable'`
Run the benchmark

`cockroach workload run tpcc --warehouses=100 --ramp=1m --duration=10m 'postgresql://root@172.28.0.5:26257?sslmode=disable'`

Per MongoDB si possono riutilizzare i container creati nei casi d'uso precedenti oppure utilizzarne dei nuovi, quindi 
eseguire docker-compose, spostarsi quindi in all'interno di py-tpcc/pytpcc ed eseguire i seguenti comandi

`python2.7 ./tpcc.py --no-execute --config=mongodb.config mongodb`

`python2.7 ./tpcc.py csv`

Comunque è possibile leggere i README presenti all'interno dei progetti scaricati.

Per MySQL, si deve importare l'immagine tpcc_server.tar scaricabile dal seguente link
https://drive.google.com/file/d/15Q5PmDMBM9PGlMrjh6d7oY85E_ueTQBZ/view?usp=sharing
quindi spostarsi all'interno di tpcc-runner ed eseguire tpcc.sh
I risultati di questo test è possibile trovarli nella cartella Risultati_TPCC
