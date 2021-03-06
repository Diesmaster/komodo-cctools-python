import os
import time
import sys
import subprocess
from slickrpc import Proxy, exc
import random

# init params, nodes amount can't be < than 5
dexp2p_clients_to_start = int(os.getenv('NODESAMOUNT'))
ac_name = 'DEXTEST'
node_ip = os.getenv('NODE_IP')
is_first_server = os.getenv('IS_FIRST')
ips_of_running_servers = []
with open("ip_list", "r") as f:
    for line in f:
        ips_of_running_servers.append(line.rstrip('\n'))

# pre-creating separate folders
for i in range(dexp2p_clients_to_start):
    os.mkdir("node_" + str(i))
    open("node_" + str(i) + "/" + ac_name + ".conf", 'a').close()
    with open("node_" + str(i) + "/" + ac_name + ".conf", 'a') as conf:
        conf.write("rpcuser=test" + '\n')
        conf.write("rpcpassword=test" + '\n')
        conf.write("rpcport=" + str(7000 + i) + '\n')
        conf.write("port=" + str(6000 + i) + '\n')

# start numnodes daemons, changing folder name and port
for i in range(dexp2p_clients_to_start):
    # first server setup - first node shouldn't have any addnode, all other clients we caonnect to the firstnode
    if is_first_server == "True":
        if i == 0:
            subprocess.call(['./komodod', '-ac_name=' + ac_name,
                             '-conf=' + sys.path[0] + '/node_' + str(i) + "/" + ac_name + ".conf",
                             '-rpcport=' + str(7000 + i), '-datadir=' + sys.path[0] + '/node_' + str(i),
                             '-ac_supply=10000000000', '-dexp2p=2', '-whitelist=127.0.0.1', '-daemon'])
            time.sleep(3)
        # let's connect first few nodes to the seed node to surely have a network
        else:
            subprocess.call(['./komodod', '-ac_name=' + ac_name,
                             '-conf=' + sys.path[0] + '/node_' + str(i) + "/" + ac_name + ".conf",
                             '-rpcport=' + str(7000 + i), '-datadir=' + sys.path[0] + '/node_' + str(i),
                             '-ac_supply=10000000000', '-dexp2p=2', '-addnode=127.0.0.1:6000', '-whitelist=127.0.0.1', '-daemon'])
            time.sleep(3)
    # not first server nodes connecting to the random nodes of already started server(s)
    else:
        daemon_args = ['./komodod', '-ac_name=' + ac_name,
                         '-conf=' + sys.path[0] + '/node_' + str(i) + "/" + ac_name + ".conf",
                         '-rpcport=' + str(7000 + i), '-datadir=' + sys.path[0] + '/node_' + str(i),
                         '-ac_supply=10000000000', '-dexp2p=2', '-whitelist=127.0.0.1', '-daemon']
        already_choosen_ports = []
        if dexp2p_clients_to_start > 4:
            # choosing 4 random pre-determined already started nodes ports to connect
            for j in range(4):
                connect_ip = random.choice(ips_of_running_servers)
                connect_port = random.randint(6000, 6000 + dexp2p_clients_to_start - 1)
                while True:
                    # to not connect to the same node twice
                    if connect_port in already_choosen_ports:
                        connect_port = random.randint(6000, 6000 + dexp2p_clients_to_start - 1)
                    else:
                        already_choosen_ports.append(connect_port)
                        break
                daemon_args.append("-addnode=" + connect_ip + ":" + str(connect_port))
        # 1 node per server mode POC
        else:
            if len(ips_of_running_servers) < 3:
                daemon_args.append("-addnode=" + ips_of_running_servers[0] + ":6000")
            else:
                already_choosen_ips = []
                for j in range(3):
                    connect_ip = random.choice(ips_of_running_servers)
                    if connect_ip in already_choosen_ips:
                        connect_ip = random.choice(ips_of_running_servers)
                    else:
                        already_choosen_ips.append(connect_ip)
                for ip in already_choosen_ips:
                    daemon_args.append("-addnode=" + ip + ":6000")
        subprocess.call(daemon_args)
        time.sleep(3)

# creating rpc proxies for all nodes
for i in range(dexp2p_clients_to_start):
    rpcport = 7000 + i
    globals()['proxy_%s' % i] = Proxy("http://%s:%s@127.0.0.1:%d" % ("test", "test", int(rpcport)))
    try:
        dex_stats_output = globals()['proxy_%s' % i].DEX_stats()
        print(dex_stats_output)
    except Exception as e:
        print(e)

# since connection ports were chosen randomly let's try to interconnect orphan nodes
for i in range(dexp2p_clients_to_start):
    connections_amount = globals()['proxy_%s' % i].getinfo()["connections"]
    print(connections_amount)

print("All nodes started (hopefully) - you can proceed to loading test")
