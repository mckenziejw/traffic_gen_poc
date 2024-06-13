from pylxd import Client

# openssl req -x509 -newkey rsa:2048 -keyout lxd.key -nodes -out lxd.crt -subj "/CN=lxd.local"

client = Client(
    endpoint='10.210.14.1:8443',
    verify=False
)

client.authenticate('lab123')
containers = client.containers.all()
for c in containers:
    print(c.name)
