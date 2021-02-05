from flask import Flask, request, jsonify
from random import randrange
import redis
from validators import LoginValidator, VerifyValidator

import requests
from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor


trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
# create a JaegerSpanExporter
jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name="auth_service",
    agent_host_name="jaeger",
    agent_port=6831,
)
span_processor = BatchExportSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask("auth_app")

FlaskInstrumentor().instrument_app(app)
RedisInstrumentor().instrument(tracer_provider=trace.get_tracer_provider())
RequestsInstrumentor().instrument()
redis_connection = redis.Redis.from_url(url="redis://redis:6379/0")


@app.route("/login/", methods=["POST"])
def login():
    data, errors = LoginValidator.validate_or_error(request.json)
    if errors:
        return jsonify(dict(errors)), 400
    login_code = str(randrange(1000, 9999))
    redis_connection.set(f"validation_code_{data['username']}", login_code)
    # dummy implementation of otp or email verification
    return jsonify(
        {
            "code": login_code,
        },
    )


@app.route("/verify/", methods=["POST"])
def verify():
    data, errors = VerifyValidator.validate_or_error(request.json)
    if errors:
        return jsonify(dict(errors)), 400
    code = redis_connection.get(f"validation_code_{data['username']}")
    if data["code"] != code.decode():
        return jsonify({"code": "invalid code"}), 400
    requests.post(url="http://point:5000/", json={**data})
    return jsonify({})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
