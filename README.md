# autoinstrumentación
install open telemetry zero-code packages.

```bash
python -m pip install opentelemetry-instrumentation \
                      opentelemetry-distro \
                      opentelemetry-exporter-otlp
```


install instrumentation libraries   

```bash 
opentelemetry-bootstrap --action=install

```

Run the app 

```bash
#NR
opentelemetry-instrument python myapp.py

```