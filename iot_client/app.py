from flask import Flask
import subprocess

def create_wpa_conf(data):
    data = f"{data}\nmac_addr=0\npreassoc_mac_addr=0\ngas_rand_mac_addr=0\n"
    return data

app = Flask(__name__)

@app.route("/update_psks", methods=['POST'])
def update_psks():
    data = request.get_json()
    psk = data['psk']
    ssid = data['ssid']
    clients = data['clients']
    for client in clients:
        c = client.instances.get('wifi-client-{}'.format(i))
        f = c.FilesManager(c)
        put_file = lambda data: f.put("/etc/wpa_supplicant/wpa_supplicant.conf",create_wpa_conf(data))
        exit_code,s_out,s_err = c.execute(
            commands = ['wpa_passphrase', ssid, psk], stdout_handler=put_file
        )
        exit_code,s_out,s_err = c.execute(
            commands = ['wpa_supplicant','-B','-i','eth1','-c','/etc/wpa_supplicant/wpa_supplicant.conf']
        )
        if(exit_code == 0):
            print('wifi-client-{} WPA supplicant successfully configured'.format(i))
        else:
            print('wifi-client-{} WPA supplicant failed'.format(i))
            print(exit_code,s_out,s_err)
        time.sleep(10)
        #pprint(c.state().network['eth1'])
        ip_assigned = False
        for a in c.state().network['eth1']['addresses']:
            if a['family'] == 'inet' and a['address'] != '':
                ip_assigned = True
                print('wifi-client-{} WPA IP Assigned'.format(i))
        if not ip_assigned:
            print('wifi-client-{} WPA DHCP did not start, running manually...'.format(i))
            exit_code,s_out,s_err = c.execute(
            commands = ['dhclient','eth1']
            )
            if(exit_code == 0):
                print('wifi-client-{} WPA DHCP manual configuration worked'.format(i))
            else:
                print('wifi-client-{} WPA DHCP manual configuration failed'.format(i))
        time.sleep(10)
        print("Updating route table")
        exit_code,s_out,s_err = c.execute(
            commands = ['ip', 'route','delete','default']
        )
        exit_code,s_out,s_err = c.execute(
            commands = ['ip', 'route','add','default', 'via', gateway]
        )
        exit_code,s_out,s_err = c.execute(
            commands = ['ip', 'link','set','eth0', 'up']
        )
        exit_code,s_out,s_err = c.execute(
            commands = ['ip', 'route','add','192.168.0.0/16', 'via', '10.120.0.1']
        )
        print("Running ping test for wifi-client-{}".format(i))
        exit_code,s_out,s_err = c.execute(
            commands = ['ping','-c', '4','8.8.8.8']
            )
        print(exit_code,s_out,s_err)
        exit_code,s_out,s_err = c.execute(
            commands = ['ping','-c', '4','192.168.10.1']
            )
        print(exit_code,s_out,s_err)

if __name__ == "__main__":
    app.run(ssl_context='adhoc')