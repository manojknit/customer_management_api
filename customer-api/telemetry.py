from opentelemetry import trace
from opentelemetry.ext import flask
from opentelemetry.exporter import jaeger
from opentelemetry.sdk import trace as sdk_trace

# Configure OpenTelemetry
trace.set_tracer_provider(sdk_trace.TracerProvider())
jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name="customer-api",
    agent_host_name="localhost",  # Change this as per your Jaeger setup
    agent_port=6831,
)

trace.get_tracer_provider().add_span_processor(
    sdk_trace.SimpleSpanProcessor(jaeger_exporter)
)

# Attach OpenTelemetry to Flask
flask.instrument_app(app)
