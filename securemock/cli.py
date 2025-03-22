# securemock/cli.py

import click
import requests
import json
import uvicorn
from securemock import server

API_URL = "http://localhost:8000/_register"

@click.group()
def cli():
    """SecureMock CLI"""
    pass

@cli.command()
@click.option("--path", required=True, help="Path to mock")
@click.option("--method", default="GET", help="HTTP method")
@click.option("--status", default=200, type=int, help="HTTP status code")
@click.option("--response", required=True, help="Mock response as JSON string")
@click.option("--expire", default=None, type=int, help="Expiration in seconds (optional)")
@click.option("--once", is_flag=True, help="Make this mock available only once")
@click.option("--match-headers", default=None, help="JSON string of headers to match")
def create(path, method, status, response, expire, once, match_headers):
    """Register a mock API endpoint"""
    try:
        headers_dict = json.loads(match_headers) if match_headers else None
        payload = {
            "path": path,
            "method": method.upper(),
            "status": status,
            "response": json.loads(response),
            "expire": expire,
            "once": once,
            "match_headers": headers_dict
        }
        r = requests.post(API_URL, json=payload)
        click.echo(f"Mock registered: {r.status_code}")
    except Exception as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind")
@click.option("--port", default=8000, help="Port to bind")
def runserver(host, port):
    """Run the FastAPI mock server"""
    uvicorn.run("securemock.server:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    cli()
