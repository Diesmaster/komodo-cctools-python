from lib import rpclib
from slickrpc import Proxy

rpc_user = "changeme"
rpc_password = "alsochangeme"
port =  24708

rpc_connect = rpc_connection = Proxy("http://%s:%s@127.0.0.1:%d"%(rpc_user, rpc_password, port));

message = "Igotabigdick"
address = "RXju6We6DDK9EYhrAVBZVXNAFbA5czw7yK"
privkey = "UsP3rR7x1t4xCa2sZGEkt5Y1BDrX5NS4u7kGfETmRkBUQ1KxZbCu"
amount = 1

stonks = rpclib.validateaddress(rpc_connect, address)

print(stonks);
