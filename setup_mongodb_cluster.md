## Set up Sharding using Docker Containers
### Config servers

Initiate replica set
```
mongo mongodb://10.27.0.2:27017
```
```
rs.initiate(
  {
    _id: "cfgsvr",
    configsvr: true,
    members: [
      { _id : 0, host : "10.27.0.2:27017" },
      { _id : 1, host : "10.27.0.3:27017" },
      { _id : 2, host : "10.27.0.4:27017" }
    ]
  }
)

rs.status()
```

### Shard 1 servers

Initiate replica set
```
mongo mongodb://10.27.0.5:27017
```
```
rs.initiate(
  {
    _id: "shard1rs",
    members: [
      { _id : 0, host : "10.27.0.5:27017" },
      { _id : 1, host : "10.27.0.6:27017" },
      { _id : 2, host : "10.27.0.7:27017" }
    ]
  }
)

rs.status()
```

## Adding another shard
### Shard 2 servers
Initiate replica set
```
mongo mongodb://10.27.0.8:27017
```
```
rs.initiate(
  {
    _id: "shard2rs",
    members: [
      { _id : 0, host : "10.27.0.8:27017" },
      { _id : 1, host : "10.27.0.9:27017" },
      { _id : 2, host : "10.27.0.10:27017" }
    ]
  }
)

rs.status()
```
### Mongos Router
### Add shard to the cluster
Connect to mongos
```
mongo mongodb://10.27.0.20:27017
```
Add shard
```
mongos> sh.addShard("shard1rs/10.27.0.5:27017,10.27.0.6:27017,10.27.0.7:27017")

mongos> sh.addShard("shard2rs/10.27.0.8:27017,10.27.0.9:27017,10.27.0.10:27017")

mongos> sh.status()
```
