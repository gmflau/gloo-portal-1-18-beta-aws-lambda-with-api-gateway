```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
   -keyout tls.key -out tls.crt -subj "/CN=*"

kubectl create -n gloo-system secret tls tls-secret --key tls.key \
   --cert tls.crt

kubectl apply -f - <<EOF
kind: Gateway
apiVersion: gateway.networking.k8s.io/v1
metadata:
  name: http
  namespace: gloo-system
spec:
  gatewayClassName: gloo-gateway
  listeners:
  - protocol: HTTPS
    port: 443
    name: https
    tls:
      mode: Terminate
      certificateRefs:
        - name: tls-secret
          kind: Secret
    allowedRoutes:
      namespaces:
        from: All
  - protocol: HTTP
    port: 8080
    name: http
    allowedRoutes:
      namespaces:
        from: All
EOF
```

```bash
kubectl apply -f- <<EOF
apiVersion: gloo.solo.io/v1
kind: Upstream
metadata:
  name: aws-rest-api-upstream
  namespace: gloo-system
spec:
  static:
    hosts:
#      - addr: cskqn8uga3.execute-api.us-west-1.amazonaws.com
      - addr: 24tpxmb55c.execute-api.us-west-1.amazonaws.com
        port: 443
    useTls: true
EOF

kubectl apply -f- <<EOF
apiVersion: gateway.networking.k8s.io/v1beta1
kind: HTTPRoute
metadata:
  name: aws-rest-api-upstream
  namespace: gloo-system
spec:
  parentRefs:
  - name: http
    namespace: gloo-system
    sectionName: https
  hostnames:
    - aws.restapi.example
  rules:
    - backendRefs:
      - name: aws-rest-api-upstream
        kind: Upstream
        group: gloo.solo.io
        port: 443
        weight: 1
      matches:
       - path:
          type: PathPrefix
          value: /prod
EOF
```

```bash
export INGRESS_GW_ADDRESS=$(kubectl get svc -n gloo-system gloo-proxy-http -o jsonpath="{.status.loadBalancer.ingress[0]['hostname','ip']}")
echo $INGRESS_GW_ADDRESS
```

```bash
curl -vik https://$INGRESS_GW_ADDRESS/prod/hello -H "host: aws.restapi.example"
```