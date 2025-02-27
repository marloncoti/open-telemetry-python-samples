import logging
import structlog
from fastapi import FastAPI, Request
import requests
import time
from opentelemetry import trace

logging.basicConfig(level=logging.INFO)



#  Get Open Telemetry Tracer
tracer = trace.get_tracer("custom-fastapi-trace")


app = FastAPI()

@app.get("/hello")
@tracer.start_as_current_span("hello_function")
async def hello():
    logger.info("Processing /hello request", trace_id=trace.get_current_span().get_span_context().trace_id)
    return {"message": "Hello, world!"}

# Custom Trace & Spam using  decorator function
@app.get("/add")
@tracer.start_as_current_span("perform_calculation")
async def add_numbers(a: int, b: int, request: Request):
    start_time = time.time()
    result = a + b
    execution_time = time.time() - start_time

    #Add Tracing Attributes
    span = trace.get_current_span()
    span.set_attribute("input.a", a)
    span.set_attribute("input.b", b)
    span.set_attribute("result", result)
    span.set_attribute("execution_time", execution_time)

    return {"operation": f"{a} + {b}", "result": result}
    

## custom Trace - traditional way-
@app.get("/search_name")
def search_name(name: str = "Kevin"):
    with tracer.start_as_current_span("search_name_request") as span:
        start_time = time.time()
        span.set_attribute("query.name", name)

        try:
            # **Nested Span for External API Call**
            with tracer.start_as_current_span("fetch_nationality_data") as api_span:
                api_start_time = time.time()
                response = requests.get(f"https://api.nationalize.io?name={name}")
                api_duration = time.time() - api_start_time

                api_span.set_attribute("http.status_code", response.status_code)
                api_span.set_attribute("api.response_time", api_duration)
                api_span.set_attribute("api.request_url", response.url)

                if response.status_code == 200:
                    result = response.json()
                    api_span.set_attribute("api.data_received", True)
                else:
                    api_span.set_attribute("api.data_received", False)
                    span.set_status(trace.Status(trace.StatusCode.ERROR, "API call failed"))
                    return {"error": "Failed to fetch data from external API"}

            # **Capture total execution time**
            total_execution_time = time.time() - start_time
            span.set_attribute("execution_time", total_execution_time)

            return result

        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            return {"error": "Unexpected error occurred"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
