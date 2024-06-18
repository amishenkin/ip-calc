from flask import Flask, render_template, request
import ipaddress

app = Flask(__name__)

def calculate_network_info(ip, prefix_length):
    network = ipaddress.IPv4Network(f"{ip}/{prefix_length}", strict=False)
    
    def to_hex(val):
        if isinstance(val, ipaddress.IPv4Address):
            return '.'.join(f'{int(octet):02X}' for octet in str(val).split('.'))
        return None
    
    def to_binary(val):
        if isinstance(val, ipaddress.IPv4Address):
            return '.'.join(f'{int(octet):08b}' for octet in str(val).split('.'))
        return None

    def get_host_min(network):
        if network.num_addresses > 2:
            return list(network.hosts())[0]
        return network.network_address

    def get_host_max(network):
        if network.num_addresses > 2:
            return list(network.hosts())[-1]
        return network.broadcast_address

    network_info = {
        "Адрес": (str(network.network_address), to_hex(network.network_address), to_binary(network.network_address)),
        "Bitmask": (prefix_length, None, None),
        "Netmask": (str(network.netmask), to_hex(network.netmask), to_binary(network.netmask)),
        "Wildcard": (str(network.hostmask), to_hex(network.hostmask), to_binary(network.hostmask)),
        "Network": (str(network.network_address), to_hex(network.network_address), to_binary(network.network_address)),
        "Broadcast": (str(network.broadcast_address), to_hex(network.broadcast_address), to_binary(network.broadcast_address)),
        "Hostmin": (str(get_host_min(network)), to_hex(get_host_min(network)), to_binary(get_host_min(network))),
        "Hostmax": (str(get_host_max(network)), to_hex(get_host_max(network)), to_binary(get_host_max(network))),
        "Hosts": (network.num_addresses - 2 if network.num_addresses > 2 else 0, None, None)
    }
    
    return network_info

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ip = request.form['ip']
        prefix_length = request.form['prefix_length']
        
        try:
            prefix_length = int(prefix_length)
            network_info = calculate_network_info(ip, prefix_length)
            return render_template('index.html', network_info=network_info)
        except ValueError:
            error = "Invalid prefix length. Please enter a number."
        except ipaddress.AddressValueError:
            error = "Invalid IP address. Please enter a valid IP address."
        
        return render_template('index.html', error=error)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)