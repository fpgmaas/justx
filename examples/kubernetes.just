# List all kubectl contexts
ctx:
    kubectl config get-contexts

# Set the current namespace
ns namespace:
    kubectl config set-context --current --namespace={{namespace}}

# List pods in a namespace
pods namespace="default":
    kubectl get pods -n {{namespace}}

# Tail logs for a pod (optionally specify container)
logs pod namespace="default" container="":
    kubectl logs -f {{pod}} -n {{namespace}} {{ if container != "" { "-c " + container } else { "" } }}

# Open a shell in a running pod
exec pod namespace="default":
    kubectl exec -it {{pod}} -n {{namespace}} -- /bin/sh

# Rollout restart a deployment
rollout deployment namespace="default":
    kubectl rollout restart deployment/{{deployment}} -n {{namespace}}

# Get events sorted by timestamp
events namespace="default":
    kubectl get events -n {{namespace}} --sort-by='.lastTimestamp'

# Show resource usage for pods
top-pods namespace="default":
    kubectl top pods -n {{namespace}}
