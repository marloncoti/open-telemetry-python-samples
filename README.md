# Auto Instrumentation
install open telemetry zero-code packages. (this packages has been added in requirement.txt file )

```bash
python -m pip install opentelemetry-instrumentation \
                      opentelemetry-distro \
                      opentelemetry-exporter-otlp
```


After install open telemetry packages , run the following command   to add extra instrumentation libs based on frameworks or libs we used in our app

```bash 
opentelemetry-bootstrap --action=install

```

set the following env Variables to configure exporter provider (honeycomb or new relic)
```bash

export OTEL_SERVICE_NAME=demo-fast-api-app
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
export OTEL_EXPORTER_OTLP_COMPRESSION=gzip
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf 
export OTEL_EXPORTER_OTLP_ENDPOINT="https://otlp.nr-data.net"
export OTEL_EXPORTER_OTLP_HEADERS="api-key=API-KEY"
export OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta


```

once extra libss were installed,  Run the app  using the following command.

```bash
# for autoinstrumentation
opentelemetry-instrument python myapp.py

```