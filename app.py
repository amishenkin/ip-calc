from flask import Flask, render_template, request
import ipaddress

app = Flask(__name__)

def calculate_network_info(ip, prefix_length):
    network = ipaddress.IPv4Network(f"{ip}/{prefix_length}", strict=False)

    network_info = {
        "IP Address": ip,
        "Prefix Length": prefix_length,
        "Network Address": network.network_address,
        "Broadcast Address": network.broadcast_address,
        "Number of Addresses": network.num_addresses,
        "Netmask": network.netmask,
        "Hostmask": network.hostmask,
        "First Host": list(network.hosts())[0] if network.num_addresses > 2 else network.network_address,
        "Last Host": list(network.hosts())[-1] if network.num_addresses > 2 else network.broadcast_address
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