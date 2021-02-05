from flask import Flask, request, jsonify
import psycopg2
from validators import AddPointValidator

from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor


from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)


jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name="point_service",
    agent_host_name="jaeger",
    agent_port=6831,
)
span_processor = BatchExportSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask("point_app")

FlaskInstrumentor().instrument_app(app)

Psycopg2Instrumentor().instrument(tracer_provider=trace.get_tracer_provider())
postgres_con = psycopg2.connect(
    database="postgres", user="postgres", host="db", port="5432",
)


@app.route("/", methods=["POST"])
def add_point():
    data, errors = AddPointValidator.validate_or_error(request.json)
    if errors:
        return jsonify(dict(errors)), 400
    with postgres_con:
        cur = postgres_con.cursor()
        cur.execute(
            f"""
                INSERT INTO user_point(username) 
                VALUES('{data["username"]}')
                ON CONFLICT (username) 
                DO NOTHING;
            """
        )
        postgres_con.commit()
    return jsonify({})


if __name__ == "__main__":
    with postgres_con:
        cur = postgres_con.cursor()
        cur.execute(
            """
                create table if not exists user_point(
                    username varchar(150) not null unique,
                    price integer DEFAULT 10
                );
            """
        )
        postgres_con.commit()
    app.run(host="0.0.0.0")
