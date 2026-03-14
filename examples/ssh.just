# Generate an ed25519 SSH key
keygen name="id_ed25519":
    ssh-keygen -t ed25519 -f ~/.ssh/{{ name }}

# Copy public key to a remote host
copy-id host:
    ssh-copy-id {{ host }}

# Open an SSH tunnel (local port forwarding)
tunnel local_port remote_host remote_port ssh_host:
    ssh -N -L {{ local_port }}:{{ remote_host }}:{{ remote_port }} {{ ssh_host }}

# Test connection to a host
test host:
    ssh -T {{ host }}

# Open SSH config in your editor
config:
    ${EDITOR:-vim} ~/.ssh/config
