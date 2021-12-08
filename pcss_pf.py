from sshtunnel import SSHTunnelForwarder
from colorama import init
from termcolor import colored
import paramiko

init()

USERNAME = "mathieum"
PCSS_KEY_PATH = "/home/mat/workfolder/home/pcss/home/.ssh/id_rsa"

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.WarningPolicy)

client.connect(
    "eagle.man.poznan.pl", port=22, username=USERNAME, key_filename=PCSS_KEY_PATH
)


def get_running_jobs():
    stdin, stdout, stderr = client.exec_command(
        "sacct -X -s running --format=JobName%60,Nodelist%10"
    )
    s = stdout.read().decode("ascii")
    out = {}
    for line in s.splitlines()[2:]:
        sl = line.split()
        sk = sl[0].split("_port:")
        if len(sk) == 2:
            out[sk[0]] = [sl[1], int(sk[1])]
        else:
            print(
                f"Found job:'{sl[0]}' on node:'{sl[1]}' but without an associated port"
            )
    return out


def start_tunnel(node, port):
    server = SSHTunnelForwarder(
        "eagle.man.poznan.pl",
        ssh_username=USERNAME,
        ssh_pkey=PCSS_KEY_PATH,
        remote_bind_address=(node, int(port)),
        mute_exceptions=True,
    )
    server.start()
    return server


def update_tunnels(t, nt):
    for k, v in t.items():  # going through old tunnels
        if k not in nt:  # job is over
            t.pop(k)[2].close()  # close this tunnel and remove it from the dict
        elif (nt[k][0] == v[0]) and (nt[k][1] == v[1]):  # job is still going
            continue
        else:  # same name as new job but different port
            t.pop(k)[2].close()  # close this tunnel and remove it from the dict

    for k, v in nt.items():  # new tunnel dict
        if k not in t:  # new job
            tun = start_tunnel(v[0], v[1])
            print(
                colored(
                    f"Adding new tunnel for job :'{k}' from '{v[0]}:{v[1]}'", "green"
                )
            )
            t[k] = [v[0], v[1], tun]
    return t


def main(tunnels):
    tunnels = update_tunnels(tunnels, get_running_jobs())

    print(colored("Current tunnels :", "cyan"))
    print("*" * 87)
    print(f"***{'':>5}JOB NAME{'':>33}***{'':>5}LOCAL URL{'':>18}***")
    print("*" * 87)
    for k, v in tunnels.items():
        print(f"***{'':>5}", end="")
        print(colored(k, "magenta"), end="")
        print(" " * (41 - len(k)), end="")
        print("***     ", end="")
        print(colored(f"http://127.0.0.1:{v[2].local_bind_port}", "blue"), end="")
        print(" " * (28 - len("http://127.0.0.1:{v[2]}")), end="")
        print("***")
        print("*" * 87)
    i = input("'q' to quit or any other key to reload the tunnels:     ")
    if i in ["q", "^C"]:
        for v in tunnels.values():
            v[2].close()
        client.close()
        print("Tunnels closed.")
    else:
        print("reloading ...")
        main(tunnels)


if __name__ == "__main__":
    try:
        main({})
    except KeyboardInterrupt:
        pass
