# Show local IP address
local-ip:
    hostname -I 2>/dev/null || ipconfig getifaddr en0

# Show public IP address
public-ip:
    curl -s https://ifconfig.me

# DNS lookup
dns host:
    dig +short {{ host }}

# Show listening ports
ports:
    ss -tlnp 2>/dev/null || lsof -iTCP -sTCP:LISTEN -nP

# Ping a host
ping host count="4":
    ping -c {{ count }} {{ host }}

# Check if a specific port is open on a host
check-port host port:
    nc -zv {{ host }} {{ port }}
