## 0 - Server preapration

Run `prepare_dexp2p_node_ms.sh`

## A - start nodes on multiply servers

1) Set NODESAMOUNT env variable 
2) Set `is_first_server` in nodes spawn script for a frist server (TODO: why it's not env?)
2.1) for each next server add new ip of previous server in ips array of spawn script

## B - spamming (after all nodes started)

1) Start spam on each  node by `./dexp2p_start_spam_ms.sh <NODEWHITEIP>`

## C - orderbooks collecting

0) Set self IP and nodes IP in `server_ips` list of `python3 dexp2p_save_orderbooks_ms.py`

1) Run `python3 dexp2p_save_orderbooks_ms.py`

packages of server's nodes will be in `packages` directory
orderbooks for each nodeip_port will be in `orderbooks` directory


## D - orderbooks parsing

1) run `python3 dexp2p_orderbooks_parser_ms.py` - it should parse files from step B into something human readable

## E - re-run tests

1) Kill all daemons (something like a `ps aux | grep DEX` and then `kill -9 {firstPID..lastPID}` or `pkill komodod` if you don't have another komodod daemons
2) ./dexp2p_clean.sh
3) return to A
