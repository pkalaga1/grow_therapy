from flask import Flask, request, jsonify
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
from wiki_gateway import WikiGateway

app = Flask(__name__)

@app.get("/")
def test_module():
    gateway = WikiGateway()
    response_json, status_code = gateway.day_of_most_views_for_article_in_given_month('Albert_Einstein', 10, 2021)
    return jsonify(response_json), status_code