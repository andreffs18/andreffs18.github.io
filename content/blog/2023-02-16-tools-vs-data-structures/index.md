---
title: Tools vs Data Structures
slug: tools-vs-data-structures
subtitle: Learning that tools don't solve all your problems
date: 2023-02-16T07:27:00+00:00
tags: [redis, postgresql, mongo, grafana, prometheus, benchmarking, data-structures, starlette, prism, openapi]
draft: false
toc: true
plotly: true
slideshow: true
image:
---

Usually, when interviewing for an engineering or software position, you end up doing some sort of "coding challenge". A friend of mine has recently left the company and is doing one at the moment. He asked me for help on solving a particular challenge, which I felt was a good exercise for me.

This blog post talks a bit about the challenge and my approach to solving it. Also, this post works as a personal reminder that sometimes it is not about picking the best tool, but the right data structure.

_"90% of the time, you can solve your problem with just the right data structures"_ - someone, once, on Reddit probably.

# The Challenge

The problem is, and I'm paraphrasing:

> _"Build a phone information aggregator API. This system takes a list of phone numbers and returns the count of valid phones broken down per prefix and business sector."_

For example, given 5 phone numbers, where 4 of them are valid, the system should return:

* a count of 1 phone for Technology, and 1 phone for Banking associated with the `+1` prefix,
* and a count of 2 phones for Clothing associated with the `+3519173` prefix.

```bash
$ curl -X POST http://localhost:8080/aggregate \
   -H 'Content-Type: application/json' \
   -d '["+1983248", "00351917355", "+147 8192", "+351917312", "+ 918851"]'
```

```json
{
  "1": {
    "Technology": 1,
    "Banking": 1
  },
  "3159173": {
    "Clothing": 2,
  }
}
```

## How to approach the problem

The problem revolves around building an API that exposes the functionality of aggregating phone numbers by industry sector. We can divide it into 4 parts:

* Expose an API through an HTTP Service
* **Check if the given phone numbers have valid prefixes**
* Interact with an external service to get the corresponding sector
* Serialize the response in the expected format

The interesting part of this problem is the 2nd step, "validate phone number prefix":

{{< mermaid >}}
sequenceDiagram
    autonumber
    actor client as Client
    participant api as Service API
    participant external as External API
    client->>api: HTTP POST /aggregate -d ["+1983236248"]
    activate client
    activate api
    alt Invalid Phone Nunber
    api->>api: Validate phone number prefix
    api->>client: HTTP 400 Bad Request
    deactivate api
    end
    activate api
    alt Valid Phone Nunber
    api->>api: Validate phone number prefix
    api->>+external: HTTP GET /sector/+1
    external->>-api: HTTP 200 OK <br>{ "number": "+1", "sector": "Technology" }
    api->>client: HTTP 200 OK <br>{ "1": { "Technology": 1 } }
    deactivate api
    end
    deactivate client
{{< /mermaid >}}

### Valid phone numbers

Validating a phone number in this context means:

* we have an extensive list of "phone prefixes" (around 900k prefixes) that should be considered the "ground truth"
* and for every given phone number, we want to cross-check against that list, and if valid, make an API call to an external service

```bash
~/projects/phone-validator $ head -n 10 prefixes.txt
1
2
44
3000000
3000001
3000002
3000003
3000004
3000005
3000006

~/projects/phone-validator $ wc -l prefixes.txt
  900005 prefixes.txt
```

So for example: If I have the phone number "+1983236248", and a list of prefixes of `[1, 2, 44]`, the prefix is "+1".

### Getting the prefix sector

To group by "sector" we need to use an external API. The OG challenge gives us an URL to use, but since that would be too much on the nose for what company this challenge is for, I'll just explain what it does 👀:

* The API has a GET request that goes to "https://a-challenge.company.com/sector/:number" where it returns the corresponding industry sector. For example: given the number `+98 72 349`, which belongs to a company in the Banking sector, the GET request to `https://a-challenge.company.com/sector/+98%2072%20349` would return the following:

```bash
$ curl https://a-challenge.company.com/sector/+98%2072%20349
{
  "number": "+9872349",
  "sector": "Banking"
}
```

{{< mermaid >}}
---
title: High-Level Architecture Diagram
---
graph LR
    API[Service]
    ExternalService[External Service]
    Client[API Client]

    Client --> | POST /aggregate | API
    subgraph 'phone-validator' Project
        API --> | Validate<br>phone number | API
    end
    API --> | Get sector | ExternalService
{{< /mermaid >}}


# Developing the API

For tackling this challenge, I'm experimenting with Starlette, which is a simple async Python framework. This project is built by following the [tutorial](https://www.starlette.io/) on Starlette documentation.

> You can find this projects codebase on https://github.com/andreffs18/phone-validator

First, we create a single `server.py` file that opens two endpoints, and starts the server:

```python
# ~/project/phone-validator/server.py
import logging
import os
import time
import uvicorn

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.routing import Route


logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)


async def startup():
    logger.info(f"Ready to start")


async def shutdown():
    logger.info("Ready to shutdown")


async def health(request):
    time.sleep(1)
    return JSONResponse({"ok": "ok"}, 200)


async def aggregate(request):
    time.sleep(1)
    return JSONResponse({"ok": "ok"}, 200)


logger.info("🌀 Starting app...")
app = Starlette(
    debug=os.environ.get("DEBUG", True),
    routes=[
        Route("/", health),
        Route("/aggregate", aggregate, methods=["POST"]),
    ],
    on_startup=[startup],
    on_shutdown=[shutdown],
)


if __name__ == "__main__":
    uvicorn.run("project.server:app", host="0.0.0.0", port=8080, reload=True)
```

To run the service just do the following:
```bash
# ~/project/phone-validator/
$ uvicorn server:app --port 8080 --host 0.0.0.0 --reload
```

And to test that everything is working, we just need to `POST /aggregate` endpoint:

```bash
~/projects/phone-validator $ curl http://localhost:8080/aggregate
{"ok": "ok"}
```

## Validating inputs

We need to check for valid phone numbers. The rules of the challenge are:

> _"A number is considered valid if it contains only digits, an optional leading `+`, and whitespace anywhere except immediately after the `+`. A valid number has exactly 3 digits or more than 6 and less than 13. `00` is acceptable as replacement for the leading `+`. All dashes and parentheses are ignored."_

This can be easily mapped to:

```python
# ~/project/phone-validator/services.py
def is_valid_phone_number(phone_number: str) -> Union[str, bool]:
    """
    A phone number is considered valid if:
    * all dashes and parentheses are ignored
    * an optional leading `+` or `00`
    * whitespace anywhere except immediately after the `+`.
    * has exactly 3 digits or more than 6 and less than 13
    * it contains only digits,
    """
    phone_number = phone_number.replace("-", "")
    phone_number = phone_number.replace("(", "")
    phone_number = phone_number.replace(")", "")

    if phone_number.startswith("+") or phone_number.startswith("00"):
        phone_number = phone_number.lstrip("+")
        phone_number = phone_number.lstrip("00")

    if phone_number.startswith(" "):
        logger.debug('number does start with " "')
        return False

    phone_number = phone_number.replace(" ", "")
    if len(phone_number) != 3:
        if not (6 < len(phone_number) < 13):
            return False

    if not phone_number.isdigit():
        logger.debug("number is not a digit")
        return False

    return phone_number
```

## Checking prefixes

The core of the problem.

In the spirit of "_let's just make this work and then improve_", we can check if a given number contains a valid prefix just by iterating through the list of prefixes and asserting that the phone number starts with that string:

```python
# ~/project/phone-validator/services.py
with open(os.path.join(os.getcwd(), "prefixes.txt")) as tmp:
    PREFIXES = list(filter(None, map(lambda line: line.strip(), tmp.readlines())))

async def get_prefix(phone_number: str) -> Union[str, bool]:
    for prefix in PREFIXES:
        if phone_number.startswith(prefix):
            return prefix
    return False
```

This is doing what we want, but it is not the best and is far from being an optimized solution.

Let's put a pin in this and revisit the topic later

## Fetching sectors

Instead of making actual requests to an external provider, we will be mocking the service using the following OpenAPI Spec:

```yaml
# ~/project/phone-validator/sector_service.yml
openapi: 3.0.3
info:
  title: Challenge Mock
  version: 1.0.0
paths:
  /sector/{phoneNumber}:
    get:
      summary: Return given's phone number sector
      parameters:
        - name: phoneNumber
          in: path
          description: Phone Number
          required: true
          schema:
            type: string
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Sector'
components:
  schemas:
    Sector:
      required:
        - number
        - sector
      type: object
      properties:
        number:
          type: string
          example: "+1478192"
        sector:
          type: string
          enum: [Auto, Banking, Energy, Health Care, Insurance, Materials, Entertainment,
            Pharmaceuticals, Real Estate, Retailing, Technology, Telecommunication,
            Transportation, Utilities]
          examples: Banking
```

I'm creating a mock service with [prism](https://github.com/stoplightio/prism). Without going into much detail, prism allows you to generate a mock/proxy server from a given OpenAPI Spec or Postman collection. It has this cool feature that makes all responses "dynamic" which provides some variability to the tests we are doing:

```bash
$ prism mock sector_service.yml --dynamic
[8:32:56 AM] › [CLI] …  awaiting  Starting Prism…
[8:32:56 AM] › [CLI] ℹ  info      GET        http://127.0.0.1:4010/sector/rem
[8:32:56 AM] › [CLI] ▶  start     Prism is listening on http://127.0.0.1:4010
```

Requesting the mock server we get:
```bash
$ curl http://127.0.0.1:4010/sector/testing
{"number": "non", "sector": "Entertainment"}

$ curl http://127.0.0.1:4010/sector/testing
{"number": "i", "sector": "Insurance"}

$ curl http://127.0.0.1:4010/sector/testing
{"number": "in", "sector": "Real Estate"}
```

Adding this external call to our project is as mapping that `curl` request into a python `request`

```python
# ~/project/phone-validator/services.py
import requests
from pydantic import BaseModel


class Response(BaseModel):
    """
    Example:
        {'number': '+1478192', 'sector': 'Clothing'}
    """
    number: str
    sector: str


async def get_sector(phone_number: str) -> str:
    response = requests.get(f"http://localhost:4010/sector/{phone_number}")
    response = Response(**response.json())
    return response.sector
```

## All together now

We have all the pieces that we need:

* The `is_valid_phone_number` method checks if the given phone number is valid
* The `get_prefix` (the part of this challenge I'm interested in exploring) finds the prefix in a given phone number and returns it
* Finally the `get_sector`, which talks to our mock server, returns a "fake" sector given a phone prefix

We are now in a condition where we can refactor our "/aggregate" route with the behavior we need:

```python
# ~/project/phone-validator/server.py
async def aggregate(request):
    phone_numbers = await request.json()
    output = {}
    for input_phone_number in phone_numbers:
        phone_number = is_valid_phone_number(phone_number=input_phone_number)
        if not phone_number:
            logger.error(f"{input_phone_number} is not valid")
            continue

        prefix = await get_prefix(phone_number=phone_number)
        if not prefix:
            logger.error(f"{phone_number} does not have a valid prefix")
            continue

        if prefix not in output:
            output[prefix] = {}
        sector = await get_sector(phone_number=phone_number)
        if sector not in output[prefix]:
            output[prefix][sector] = 0

        output[prefix][sector] += 1

    return JSONResponse(output, 200)
```


Spinning up our service, and making the original request from the challenge instructions, gives us this:

```bash
$ curl -X POST http://localhost:8080/aggregate \
   -H 'Content-Type: application/json' \
   -d '["+1983248", "00351917355", "+147 8192", "+351917312", "+ 918851"]' | jq

{
  "1": {
    "Banking": 1,
    "Utilities": 1
  },
  "3519173": {
    "Auto": 2
  }
}
```

# Benchmarking this solution

Thinking back on the solution we have, the `get_prefix` that we've implemented is arguably not the best approach. That is the point of this blog post: What is the most performant solution for this problem? But first, how bad is this solution?

* Is this slow, and how slow? In the worst-case scenario (ie: validating the last prefix) how much time it takes?
* Is the `PREFIX` list that big of a memory footprint? Or is it just a couple of kilobytes?
* How many parallel requests am I able to serve with this solution?

To do this assessment I restructured the project and added some extra functionality:

* Create `routes.py` file where the `aggregate()` and `health()` routers live
* Created a new `backend/` folder where I abstracted the function `get_prefix` into the file `backend/in_memory.py`
* Configured the `startup()` even hook of the Starlette server to choose its "backend" using an environment variable
* Added docker-compose to the project so I can start the whole project with just `docker-compose up`
* Initialized `prometheus-middleware` on the Startlette app, so we can have a `/metrics` endpoint to have some observability using Grafana dashboards

This is what the project looks like now:

```bash
# ~/project/phone-validator/
.
├── README.md
├── Dockerfile
├── sector_service.yml
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
├── prefixes.txt
├── backends
│   └── in_memory
│       ├── def get_prefix()
│       ├── def startup_backend()
│       └── def shutdown_backend()
├── server.py
│   ├── def startup()
│   ├── def shutdown()
│   └── def init_server()
├── routes.py
│   ├── def health()
│   └── def aggregate()
└── services.py
    ├── def is_valid_phone_number()
    └── def get_sector()
```

```yml
# ~/project/phone-validator/docker-compose.yml
version: "3.2"
services:
  prometheus:
    image: prom/prometheus:v2.30.3
    ports:
      - 9000:9090
    volumes:
      - ./tmp/prometheus:/etc/prometheus
      - ./tmp/prometheus/prometheus-data:/prometheus
    command: --web.enable-lifecycle  --config.file=/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - 3000:3000
    volumes:
      - ./tmp/grafana/provisioning/datasources:/etc/grafana/provisioning/datasources
      - ./tmp/grafana/grafana-data:/var/lib/grafana
    environment:
      - GF_DEFAULT_APP_MODE=development
    depends_on:
      - prometheus

  api:
    restart: always
    build:
      context: .
      dockerfile: Dockerfile
    depends_on:
      - mock
      - grafana
    ports:
      - 8080:8080
    volumes:
      - .:/app/

  mock:
    image: stoplight/prism
    ports:
      - 4010:4010
    volumes:
      - ./sector_service.yml:/usr/src/prism/packages/cli/sector_service.yml
    command: mock sector_service.yml --dynamic --host 0.0.0.0
```

> To find the grafana dashboard or check the project's code, you can go here: https://github.com/andreffs18/phone-validator


## Qualifying the solution

Let's take a look question by question:

### Is this slow, and how slow? In the worst-case scenario (ie: last prefix) how much time it takes?

We can see this by measuring the time it takes to get a response. This involves all of the steps of requests on the sequence diagram below:

{{< mermaid >}}
sequenceDiagram
    autonumber
    actor client as Client
    participant api as Service API
    participant external as External API
    client->>api: HTTP POST /aggregate -d ["+1983236248"]
    activate client
    activate api
    api->>api: Validate phone number prefix
    api->>+external: HTTP GET /sector/+1
    external->>-api: HTTP 200 OK <br>{ "number": "+1", "sector": "Technology" }
    api->>client: HTTP 200 OK <br>{ "1": { "Technology": 1 } }
    deactivate api
    deactivate client
{{< /mermaid >}}


To test this we will monitor the "Requests Time Taken" panel on our Grafana dashboard, which tells us how much time each request takes, plus we will be using "[hey](https://github.com/rakyll/hey)" to benchmark the endpoint.

> A quick side note: with this blog post I ended up spending most of the time playing around with benchmarking tools and afaik hey [doesn't handle well high concurrency levels](https://github.com/rakyll/hey/issues/71). So if your planing on doing some _heavy loads_, the recommended alternative is [apache benchmark](https://httpd.apache.org/docs/2.4/programs/ab.html).

The question we want to answer is: What's the P95 of the `/aggregate` endpoint, with a phone number that has the first, middle, or last prefix of the list?

```bash
# How many elements in the prefixes list
$ wc -l prefixes.txt
  900005 prefixes.txt

# First valid prefix
$ head -n1 prefixes.txt
1

# Last valid prefix
$ tail -n1 prefixes.txt
6

# Prefix in the middle of the list
# $ head -n (900005/2) prefixes.txt | tail -n1
$ head -n450002 prefixes.txt| tail -n1
3449998
```

For 60 seconds, we ran the following command simulating one HTTP client with the number `+1983248`, then `+344999813123`, and lastly `+6983248`.

```bash
$ hey -z 60s -c 1 -m GET \
  -H "Content-Type: application/json" \
  -d '["{{ NUMBER }}"]' \
  http://localhost:8080/aggregate
```

> Keep in mind that this was done on my Laptop, a 2015 MacBook Pro with 3.1 GHz Dual Core Intel i7, with 16GB of memory.


{{< slideshow timetaken >}}
[
  {url: "images/time-taken-1-global.png"},
  {url: "images/time-taken-2-+1-prefix.png"},
  {url: "images/time-taken-3-+3449998-prefix.png"},
  {url: "images/time-taken-4-+6-prefix.png"}
]
{{< /slideshow >}}

| Prefix | Req/s | P95 | Total Reqs |
| ----- | ----- | ----- | ----- |
| +1983248 (first) | 27.7820 | 0.0731 secs | 1668 responses |
| +344999813123 (middle) | 6.8536 | 0.2894 secs | 412 responses |
| +6983248 (last) | 4.0407 | 0.4103 secs | 243 responses |

Answering our question, we can see that with the current implementation, when we validate the phone prefix, the further away we are from the beginning of the `"PREFIX"` list, the slower the API takes to handle the request. Concretely, we get a 7X performance hit on the P95 of the service, depending on the input.

### Is the `PREFIX` list that big of a memory footprint?

Looking at our "Services Memory" panel, we can see how much loading all prefixes into memory users from our available memory.

{{< slideshow memory-footprint >}}
[
  {url: "images/memory-global-view.png", description: "Before and after storing the 900k prefixes in memory." },
  {url: "images/memory-before.png", description: "66 MBs increase (From 122 MBs to 188 MBs)"},
  {url: "images/memory-after.png", description: "66 MBs increase (From 122 MBs to 188 MBs)"}
]
{{< /slideshow >}}

### How many parallel requests am I able to serve with this solution?

Similar to the question above, how many requests can this solution handle during 60 seconds by either having 2, 4, or 8 concurrent clients making those requests?

**Baseline: 1 client**

| Solution | Clients | Prefix | Req/s | P95 | Total Reqs |
| ----- | ----- | ----- | ----- | ----- | ----- |
| in_memory | c1 | +1983248 (first) | 27.7820 | 0.0731 secs | 1668 responses |
| in_memory | c1 | +344999813123 (middle) | 6.8536 | 0.2894 secs | 412 responses |
| in_memory | c1 | +6983248 (last) | 4.0407 | 0.4103 secs | 243 responses |
| in_memory | c2 | +1983248 | 48.3398 | 0.0836 secs | 2902 responses |
| in_memory | c2 | +344999813123 | 9.4420 | 0.4440 secs | 568 responses |
| in_memory | c2 | +6983248 | 4.3614 | 0.8041 secs | 263 responses |
| in_memory | c4 | +1983248 | 59.2556 | 0.1272 secs | 3558 responses |
| in_memory | c4 | +344999813123 | 9.5636 | 0.6002 secs | 577 responses |
| in_memory | c4 | +6983248 | 3.8022 | 1.8013 secs | 232 responses |
| in_memory | c8 | +1983248 | 46.7732 | 0.3957 secs | 2814 responses |
| in_memory | c8 | +344999813123 | 7.9378 | 1.4435 secs | 481 responses |
| in_memory | c8 | +6983248 | 2.3447 | 9.0418 secs | 144 responses |


{{< plotly benchmark-rps>}}
{"data":[{"alignmentgroup":"True","bingroup":"x","histfunc":"sum","hovertemplate":"clients=c1<br>prefix=%{x}<br>sum of totals=%{y}<extra></extra>","legendgroup":"c1","marker":{"color":"rgb(99,110,251)","pattern":{"shape":""}},"name":"c1","offsetgroup":"c1","orientation":"v","showlegend":true,"x":["+1983248","+344999813123","+6983248"],"xaxis":"x","y":[1931,527,304],"yaxis":"y","type":"histogram"},{"alignmentgroup":"True","bingroup":"x","histfunc":"sum","hovertemplate":"clients=c2<br>prefix=%{x}<br>sum of totals=%{y}<extra></extra>","legendgroup":"c2","marker":{"color":"rgb(233,86,63)","pattern":{"shape":""}},"name":"c2","offsetgroup":"c2","orientation":"v","showlegend":true,"x":["+1983248","+344999813123","+6983248"],"xaxis":"x","y":[3468,384,331],"yaxis":"y","type":"histogram"},{"alignmentgroup":"True","bingroup":"x","histfunc":"sum","hovertemplate":"clients=c4<br>prefix=%{x}<br>sum of totals=%{y}<extra></extra>","legendgroup":"c4","marker":{"color":"rgb(0,204,150)","pattern":{"shape":""}},"name":"c4","offsetgroup":"c4","orientation":"v","showlegend":true,"x":["+1983248","+344999813123","+6983248"],"xaxis":"x","y":[4101,591,339],"yaxis":"y","type":"histogram"},{"alignmentgroup":"True","bingroup":"x","histfunc":"sum","hovertemplate":"clients=c8<br>prefix=%{x}<br>sum of totals=%{y}<extra></extra>","legendgroup":"c8","marker":{"color":"rgb(171,99,250)","pattern":{"shape":""}},"name":"c8","offsetgroup":"c8","orientation":"v","showlegend":true,"x":["+1983248","+344999813123","+6983248"],"xaxis":"x","y":[4248,604,328],"yaxis":"y","type":"histogram"}],"layout":{"template":{"data":{"histogram2dcontour":[{"type":"histogram2dcontour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"choropleth":[{"type":"choropleth","colorbar":{"outlinewidth":0,"ticks":""}}],"histogram2d":[{"type":"histogram2d","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmap":[{"type":"heatmap","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmapgl":[{"type":"heatmapgl","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"contourcarpet":[{"type":"contourcarpet","colorbar":{"outlinewidth":0,"ticks":""}}],"contour":[{"type":"contour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"surface":[{"type":"surface","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"mesh3d":[{"type":"mesh3d","colorbar":{"outlinewidth":0,"ticks":""}}],"scatter":[{"fillpattern":{"fillmode":"overlay","size":10,"solidity":0.2},"type":"scatter"}],"parcoords":[{"type":"parcoords","line":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolargl":[{"type":"scatterpolargl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"scattergeo":[{"type":"scattergeo","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolar":[{"type":"scatterpolar","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"scattergl":[{"type":"scattergl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatter3d":[{"type":"scatter3d","line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermapbox":[{"type":"scattermapbox","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterternary":[{"type":"scatterternary","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattercarpet":[{"type":"scattercarpet","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"type":"carpet"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}],"barpolar":[{"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"pie":[{"automargin":true,"type":"pie"}]},"layout":{"autotypenumbers":"strict","colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"hovermode":"closest","hoverlabel":{"align":"left"},"paper_bgcolor":"white","plot_bgcolor":"#E5ECF6","polar":{"bgcolor":"#E5ECF6","angularaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"radialaxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"ternary":{"bgcolor":"#E5ECF6","aaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"baxis":{"gridcolor":"white","linecolor":"white","ticks":""},"caxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]]},"xaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"yaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"scene":{"xaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"yaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"zaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"geo":{"bgcolor":"white","landcolor":"#E5ECF6","subunitcolor":"white","showland":true,"showlakes":true,"lakecolor":"white"},"title":{"x":0.05},"mapbox":{"style":"light"}}},"xaxis":{"anchor":"y","domain":[0.0,1.0],"title":{"text":""},"type":"category"},"yaxis":{"anchor":"x","domain":[0.0,1.0],"title":{"text":"sum of totals"}},"legend":{"title":{"text":"clients"},"tracegroupgap":0},"title":{"text":"Total requests for \"In Memory\", during 60 seconds","font":{"size":30}},"barmode":"group","margin":{"b":80,"l":80,"r":80,"t":100,"pad":2},"updatemenus":[{"buttons":[{"args":[{"x":[["+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248"]]},{"xaxis":{"title":"","type":"category"}}],"label":"Phone Prefix","method":"update"}],"direction":"down","showactive":true,"xanchor":"left","yanchor":"bottom"}],"plot_bgcolor":"rgba(236, 236, 236, 0.3)","width":825}}
{{< /plotly >}}


Similar to our first question, the further away we are from the beginning of the `“PREFIX”` list, the least amount of requests we can handle in parallel.

# Alternatives

Of course, if I were to submit this challenge, this would not be the solution that I would be most proud of... in a nutshell, it doesn't scale (slow and would need many instances to support the increased load).

Although very simple, it's naive to assume that we would want to do string comparisons on a set of 900k elements for every request we get, on a possible very busy service.

So how can I solve this? Well:
* My first thought is to use a database and leverage its capabilities of searching + indexing.
* My second thought (and to be honest, going back to my "Algorithms and Data Structures" book) is to find a better data structure that solves this problem cleanly

To answer the first idea, I'll be using Mongo, Postgres, and Redis databases to check the differences in RPS, P95, and Total Requests. For the second one, I'll be comparing the original "In Memory" with a "Trie" data structure.


## Setting up backends

Not spending too much time showing the setup of these solutions as before (the code can be found in the [repo](https://github.com/andreffs18/phone-validator)) but for all these different solutions I did:

* Installed the dependencies to be able to play with the different solutions
* Added new files to the `backend/` folder to then initialize each solution using a .env variable
* Added both the database + an open-source dashboard to my docker-compose so I could see what was going on

{{< highlight bash "hl_lines=13-20" >}}
# ~/project/phone-validator/
.
├── README.md
├── Dockerfile
├── sector_service.yml
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
├── prefixes.txt
├── backends
│   ├── in_memory
│   │   └── (...)
│   ├── trie
│   │   └── (...)
│   ├── mongo
│   │   └── (...)
│   ├── postgres
│   │   └── (...)
│   └── redis
│       └── (...)
├── server.py
│   ├── def startup()
│   ├── def shutdown()
│   └── def init_server()
├── routes.py
│   ├── def health()
│   └── def aggregate()
└── services.py
    ├── def is_valid_phone_number()
    └── def get_sector()
{{< /highlight >}}


{{< mermaid >}}
---
title: High-Level Architecture Diagram
---

graph LR
    Redis[(Redis)]
    Postgres[(Postgres)]
    Mongo[(MongoDB)]
    API[Starlette API]
    InMemory([In Memory])
    Trie([Trie])
    ExternalService
    Client[API Client]
    Client --> | POST /aggregate | API
    subgraph 'phone-validator' Project
        API <--> | Validate<br>phone number | Mongo
        API <--> | Validate<br>phone number | Postgres
        API <--> | Validate<br>phone number | Redis
        API <-.->| Validate<br>phone number | InMemory
        API <-.->| Validate<br>phone number | Trie
    end
    API ---> | Get sector | ExternalService
{{< /mermaid >}}


## Using databases

### Mongo

For Mongo, I just added all prefixes to a collection with the key "prefix", and make an `$in` query with the "exploded" number.

```python
# ~/project/phone-validator/backends/mongo.py
import motor.motor_asyncio
from services import read_prefix_file


async def get_prefix(request, phone_number: str) -> Union[str, bool]:
    mongo_client = motor.motor_asyncio.AsyncIOMotorClient("mongo", 27017)
    # explode phone number in a list of sub-numbers
    # eg: phone_number = "1234" -> ["1234", "123", "12", "1"]
    prefixes = [phone_number[:index] for index in range(len(phone_number), 0, -1)]
    result = await mongo_client.test.test_value.find_one({"prefix": {"$in": prefixes}})
    if not result:
        return False

    return result["prefix"]


async def startup_backend(app: Starlette, logger: Logger) -> None:
    mongo_client = motor.motor_asyncio.AsyncIOMotorClient("mongo", 27017)
    # create index on prefix column with ascending sort order
    await mongo_client.test.test_value.create_index([("prefix", "1")], background=False)

    prefixes = read_prefix_file()
    # one object per key, with the actual line being the value of the "key" field
    await mongo_client.test.test_value.insert_many(map(lambda prefix: {"prefix": prefix}, prefixes))
    # deallocate memory from a list of 900k prefixes
    del prefixes
    logger.info('Ready to go with mongo database "test"')
```

### Postgres

For Postgres, I've also initialized the DB with a "prefix" column and added all prefixes but the approach to query is a bit different:
* Find in the "prefix" table a "phone number" that "LIKE"s each prefix.
* Because there might be more than one (ie: "+344999813123" find prefixes "1", "2", "44", "3449998"), we want to get the "longest common string" which would be the last one of the ordered list.

```python
# ~/project/phone-validator/backends/postgres.py
import psycopg

from services import read_prefix_file


async def get_prefix(request, phone_number: str) -> Union[str, bool]:
    async with await psycopg.AsyncConnection.connect("postgresql://postgres:postgres@postgres:5432/postgres") as postgres_client:
        async with postgres_client.cursor() as cur:
            await cur.execute(
                f"SELECT * FROM prefix WHERE '{phone_number}' LIKE '%' || prefix || '%' ORDER BY prefix DESC LIMIT 1"
            )
            result = await cur.fetchone()

    if not result:
        return False
    return result[0]


async def startup_backend(app: Starlette, logger: Logger) -> None:
    prefixes = read_prefix_file()

    async with await psycopg.AsyncConnection.connect("postgresql://postgres:postgres@postgres:5432/postgres") as postgres_client:
        async with postgres_client.cursor() as cur:
            await cur.execute("CREATE TABLE IF NOT EXISTS prefix (prefix INT PRIMARY KEY NOT NULL);")

            amount = 5000
            chunks = [prefixes[i : i + amount] for i in range(0, len(prefixes), amount)]
            for prefixes in chunks:
                prefixes = ",".join([f"({prefix})" for prefix in prefixes])
                # setup column "prefix" with all lines as rows
                await cur.execute(f"INSERT INTO prefix (prefix) VALUES {prefixes} ON CONFLICT (prefix) DO NOTHING;")

    logger.info('Ready to go with postgres database "postgres"')
```

### Redis (is it a database?)

For Redis, the simplest way I could find was to mimic the solution I did for Mongo:
* add all prefixes to a key as a member,
* then we can use the `smismember` command to check if a given list of values belongs to the set.

That returns a list of "0's" and "1's" that match the list of "exploded prefixes", so just doing an XOR between the results and our "exploded number", gives us our prefix

```python
# ~/project/phone-validator/backends/redis.py
import redis
from services import read_prefix_file


async def get_prefix(request, phone_number: str) -> Union[str, bool]:
    r = redis.Redis(host="redis", port=6379, db=0)
    # explode phone number in a list of sub-numbers
    # eg: phone_number = "1234" -> ["1234", "123", "12", "1"]
    prefixes = [phone_number[:index] for index in range(len(phone_number), 0, -1)]
    result = r.smismember("prefix", prefixes)
    # parse zipped list of prefixes with an array of returned booleans
    # eg: zip(["1234", "123", "12", "1"], [0, 0, 0, 1]) => ["1"]
    result = list([p for p, r in zip(prefixes, result) if r])
    if not result:
        return False
    return result[0]


async def startup_backend(app: Starlette, logger: Logger) -> None:
    r = redis.Redis(host="redis", port=6379, db=0)

    prefixes = read_prefix_file()
    # create set "prefix" and add all lines as members.
    r.sadd("prefix", *prefixes)
    logger.info('Ready to go with redis database "0"')
```

## Using data structures

### Trie structure

Trie is [more than a binary tree](https://en.wikipedia.org/wiki/Trie) and the thing to notice is that with this data structure (compared against the original "in_memory" solution) our memory footprint increases a lot.

> "A naive implementation of a trie consumes immense storage due to larger number of leaf-nodes caused by sparse distribution of keys" - [Wikipedia](https://en.wikipedia.org/wiki/Trie#Patricia_trees)

The best part of this solution is that it keeps operations to find a valid prefix in constant time.

```python
# ~/project/phone-validator/backends/trie.py
from pytrie import StringTrie
from services import read_prefix_file


async def get_prefix(request, phone_number: str) -> Union[str, bool]:
    return request.app.state.trie.longest_prefix(phone_number, default=None)


async def startup_backend(app: Starlette, logger: Logger) -> None:
    trie = StringTrie()
    for p in read_prefix_file():
        trie[p] = True

    app.state.trie = trie
    logger.info(f"Ready to go with {len(app.state.trie)} lines")
```


## Comparing results

The same tests were made: for each solution, during 60 seconds, simulate 1, 2, 4, and 8 concurrent clients, asking for the first, middle, and last prefix of the list.

This bash script should handle this nicely:
```bash
# ~/project/phone-validator/loadtest/run.sh
#!/bin/bash
for MODE in "in_memory" "trie" "mongo" "postgres" "redis"
do
    mkdir loadtest/$MODE;
    echo "👀 Starting \"$MODE\" load test..."
    echo "BACKEND=backend.$MODE" >> .env
    source .env
    docker-compose --env-file .env up -d
    echo "Sleeping for 60 to let server bootstrap"
    sleep 60

    for number in "+1983248" "+344999813123" "+6983248"
    do
        for clients in 1 2 4 8
        do
            echo "Running for 60seconds '-c $clients' for '$number' ..."
            hey -z 60s -c $clients -m POST -H "Content-Type: application/json" \
                -d "[\"$number\"]" http://localhost:8080/aggregate > loadtest/$MODE/output-c$clients-$number.txt
            echo "Sleeping for 60"
            sleep 60
        done
    done

    # Print RPS, P95 and Total Requests once finished
    for file in loadtest/$MODE/*.txt; do
        echo $file
        cat $file | sed -n -e 7p -e 32p -e 43p
        echo ""
    done
done
```

{{< plotly conclusion >}}
{"data":[{"alignmentgroup":"True","bingroup":"x","histfunc":"sum","hovertemplate":"solution=in_memory<br>prefix=%{x}<br>sum of totals=%{y}<extra></extra>","legendgroup":"in_memory","marker":{"color":"rgb(0,204,150)","pattern":{"shape":""}},"name":"in_memory","offsetgroup":"in_memory","orientation":"v","showlegend":true,"x":["+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248"],"xaxis":"x","y":[1931,527,304,3468,384,331,4101,591,339,4248,604,328],"yaxis":"y","type":"histogram"},{"alignmentgroup":"True","bingroup":"x","histfunc":"sum","hovertemplate":"solution=trie<br>prefix=%{x}<br>sum of totals=%{y}<extra></extra>","legendgroup":"trie","marker":{"color":"rgb(171,99,250)","pattern":{"shape":""}},"name":"trie","offsetgroup":"trie","orientation":"v","showlegend":true,"x":["+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248"],"xaxis":"x","y":[2313,2317,1760,3567,3545,2703,5133,5110,3187,5210,3051,3176],"yaxis":"y","type":"histogram"},{"alignmentgroup":"True","bingroup":"x","histfunc":"sum","hovertemplate":"solution=mongo<br>prefix=%{x}<br>sum of totals=%{y}<extra></extra>","legendgroup":"mongo","marker":{"color":"rgb(233,86,63)","pattern":{"shape":""}},"name":"mongo","offsetgroup":"mongo","orientation":"v","showlegend":true,"x":["+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248"],"xaxis":"x","y":[1075,1263,940,1413,1246,1057,1500,1175,1122,1563,1151,1172],"yaxis":"y","type":"histogram"},{"alignmentgroup":"True","bingroup":"x","histfunc":"sum","hovertemplate":"solution=postgres_async<br>prefix=%{x}<br>sum of totals=%{y}<extra></extra>","legendgroup":"postgres_async","marker":{"color":"rgb(255,161,90)","pattern":{"shape":""}},"name":"postgres_async","offsetgroup":"postgres_async","orientation":"v","showlegend":true,"x":["+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248"],"xaxis":"x","y":[116,199,118,182,303,188,175,324,193,184,313,194],"yaxis":"y","type":"histogram"},{"alignmentgroup":"True","bingroup":"x","histfunc":"sum","hovertemplate":"solution=redis<br>prefix=%{x}<br>sum of totals=%{y}<extra></extra>","legendgroup":"redis","marker":{"color":"rgb(99,110,251)","pattern":{"shape":""}},"name":"redis","offsetgroup":"redis","orientation":"v","showlegend":true,"x":["+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248"],"xaxis":"x","y":[1948,1992,2074,2885,2894,2832,3974,3966,3975,4147,3940,4040],"yaxis":"y","type":"histogram"}],"layout":{"template":{"data":{"histogram2dcontour":[{"type":"histogram2dcontour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"choropleth":[{"type":"choropleth","colorbar":{"outlinewidth":0,"ticks":""}}],"histogram2d":[{"type":"histogram2d","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmap":[{"type":"heatmap","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmapgl":[{"type":"heatmapgl","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"contourcarpet":[{"type":"contourcarpet","colorbar":{"outlinewidth":0,"ticks":""}}],"contour":[{"type":"contour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"surface":[{"type":"surface","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"mesh3d":[{"type":"mesh3d","colorbar":{"outlinewidth":0,"ticks":""}}],"scatter":[{"fillpattern":{"fillmode":"overlay","size":10,"solidity":0.2},"type":"scatter"}],"parcoords":[{"type":"parcoords","line":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolargl":[{"type":"scatterpolargl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"scattergeo":[{"type":"scattergeo","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolar":[{"type":"scatterpolar","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"scattergl":[{"type":"scattergl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatter3d":[{"type":"scatter3d","line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermapbox":[{"type":"scattermapbox","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterternary":[{"type":"scatterternary","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattercarpet":[{"type":"scattercarpet","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"type":"carpet"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}],"barpolar":[{"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"pie":[{"automargin":true,"type":"pie"}]},"layout":{"autotypenumbers":"strict","colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"hovermode":"closest","hoverlabel":{"align":"left"},"paper_bgcolor":"white","plot_bgcolor":"#E5ECF6","polar":{"bgcolor":"#E5ECF6","angularaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"radialaxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"ternary":{"bgcolor":"#E5ECF6","aaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"baxis":{"gridcolor":"white","linecolor":"white","ticks":""},"caxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]]},"xaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"yaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"scene":{"xaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"yaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"zaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"geo":{"bgcolor":"white","landcolor":"#E5ECF6","subunitcolor":"white","showland":true,"showlakes":true,"lakecolor":"white"},"title":{"x":0.05},"mapbox":{"style":"light"}}},"xaxis":{"anchor":"y","domain":[0.0,1.0],"title":{"text":""},"type":"category"},"yaxis":{"anchor":"x","domain":[0.0,1.0],"title":{"text":"sum of totals"}},"legend":{"title":{"text":"solution"},"tracegroupgap":0},"title":{"text":"Total requests, during 60 seconds","font":{"size":30}},"barmode":"group","margin":{"b":80,"l":80,"r":80,"t":100,"pad":2},"updatemenus":[{"buttons":[{"args":[{"x":[["+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248","+1983248","+344999813123","+6983248"]]},{"xaxis":{"title":"","type":"category"}}],"label":"Phone Prefix","method":"update"},{"args":[{"x":[["c1","c1","c1","c2","c2","c2","c4","c4","c4","c8","c8","c8","c1","c1","c1","c2","c2","c2","c4","c4","c4","c8","c8","c8","c1","c1","c1","c2","c2","c2","c4","c4","c4","c8","c8","c8","c1","c1","c1","c2","c2","c2","c4","c4","c4","c8","c8","c8","c1","c1","c1","c2","c2","c2","c4","c4","c4","c8","c8","c8"]]},{"xaxis":{"title":"","type":"category"}}],"label":"HTTP Clients","method":"update"}],"direction":"down","showactive":true,"xanchor":"left","yanchor":"bottom"}],"plot_bgcolor":"rgba(236, 236, 236, 0.3)","width":825}}
{{< /plotly >}}


{{< slideshow slide-conclusion >}}
[
  {url: "images/grafana-global.png"},
  {url: "images/grafana-in-memory.png"},
  {url: "images/grafana-trie.png"},
  {url: "images/grafana-mongo.png"},
  {url: "images/grafana-postgres.png"},
  {url: "images/grafana-redis.png"},
  {url: "images/grafana-global-highlighted.png"},
]
{{< /slideshow >}}


{{< plotly memory >}}
{"data":[{"alignmentgroup":"True","bingroup":"x","histfunc":"avg","hovertemplate":"solution=%{x}<br>avg of vm_mbytes=%{y}<extra></extra>","legendgroup":"in_memory","marker":{"color":"rgb(0,204,150)","pattern":{"shape":""}},"name":"in_memory","offsetgroup":"in_memory","orientation":"v","showlegend":true,"x":["in_memory","in_memory","in_memory","in_memory","in_memory","in_memory","in_memory","in_memory","in_memory","in_memory","in_memory","in_memory"],"xaxis":"x","y":[252.171875,5.420898438,614.09375,324.6835938,5.420898438,614.09375,468.8203125,5.420898438,614.09375,5.420898438,614.09375,686.0976563],"yaxis":"y","type":"histogram"},{"alignmentgroup":"True","bingroup":"x","histfunc":"avg","hovertemplate":"solution=%{x}<br>avg of vm_mbytes=%{y}<extra></extra>","legendgroup":"trie","marker":{"color":"rgb(171,99,250)","pattern":{"shape":""}},"name":"trie","offsetgroup":"trie","orientation":"v","showlegend":true,"x":["trie","trie","trie","trie","trie","trie","trie","trie","trie","trie","trie","trie"],"xaxis":"x","y":[481.3046875,556.6367188,631.28125,554.3242188,556.6367188,631.28125,555.8671875,630.0820313,631.28125,556.6367188,631.28125,703.2851563],"yaxis":"y","type":"histogram"},{"alignmentgroup":"True","bingroup":"x","histfunc":"avg","hovertemplate":"solution=%{x}<br>avg of vm_mbytes=%{y}<extra></extra>","legendgroup":"mongo","marker":{"color":"rgb(233,86,63)","pattern":{"shape":""}},"name":"mongo","offsetgroup":"mongo","orientation":"v","showlegend":true,"x":["mongo","mongo","mongo","mongo","mongo","mongo","mongo","mongo","mongo","mongo","mongo","mongo"],"xaxis":"x","y":[1806.675781,1878.894531,1782.847656,1830.6875,1862.886719,1822.867188,1662.605469,181.4863281,1830.871094,193.4921875,181.4863281,1798.855469],"yaxis":"y","type":"histogram"},{"alignmentgroup":"True","bingroup":"x","histfunc":"avg","hovertemplate":"solution=%{x}<br>avg of vm_mbytes=%{y}<extra></extra>","legendgroup":"postgres_async","marker":{"color":"rgb(255,161,90)","pattern":{"shape":""}},"name":"postgres_async","offsetgroup":"postgres_async","orientation":"v","showlegend":true,"x":["postgres_async","postgres_async","postgres_async","postgres_async","postgres_async","postgres_async","postgres_async","postgres_async","postgres_async","postgres_async","postgres_async","postgres_async"],"xaxis":"x","y":[216.3007813,576.8203125,648.8242188,288.3046875,576.8203125,648.8242188,432.5625,576.8203125,648.8242188,576.8203125,648.8242188,648.8242188],"yaxis":"y","type":"histogram"},{"alignmentgroup":"True","bingroup":"x","histfunc":"avg","hovertemplate":"solution=%{x}<br>avg of vm_mbytes=%{y}<extra></extra>","legendgroup":"redis","marker":{"color":"rgb(99,110,251)","pattern":{"shape":""}},"name":"redis","offsetgroup":"redis","orientation":"v","showlegend":true,"x":["redis","redis","redis","redis","redis","redis","redis","redis","redis","redis","redis","redis"],"xaxis":"x","y":[275.4023438,564.1679688,564.1679688,0.34765625,564.1679688,564.1679688,491.6640625,564.1679688,564.1679688,564.1679688,564.1679688,63.6171875],"yaxis":"y","type":"histogram"}],"layout":{"template":{"data":{"histogram2dcontour":[{"type":"histogram2dcontour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"choropleth":[{"type":"choropleth","colorbar":{"outlinewidth":0,"ticks":""}}],"histogram2d":[{"type":"histogram2d","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmap":[{"type":"heatmap","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmapgl":[{"type":"heatmapgl","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"contourcarpet":[{"type":"contourcarpet","colorbar":{"outlinewidth":0,"ticks":""}}],"contour":[{"type":"contour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"surface":[{"type":"surface","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"mesh3d":[{"type":"mesh3d","colorbar":{"outlinewidth":0,"ticks":""}}],"scatter":[{"fillpattern":{"fillmode":"overlay","size":10,"solidity":0.2},"type":"scatter"}],"parcoords":[{"type":"parcoords","line":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolargl":[{"type":"scatterpolargl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"scattergeo":[{"type":"scattergeo","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolar":[{"type":"scatterpolar","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"scattergl":[{"type":"scattergl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatter3d":[{"type":"scatter3d","line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermapbox":[{"type":"scattermapbox","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterternary":[{"type":"scatterternary","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattercarpet":[{"type":"scattercarpet","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"type":"carpet"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}],"barpolar":[{"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"pie":[{"automargin":true,"type":"pie"}]},"layout":{"autotypenumbers":"strict","colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"hovermode":"closest","hoverlabel":{"align":"left"},"paper_bgcolor":"white","plot_bgcolor":"#E5ECF6","polar":{"bgcolor":"#E5ECF6","angularaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"radialaxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"ternary":{"bgcolor":"#E5ECF6","aaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"baxis":{"gridcolor":"white","linecolor":"white","ticks":""},"caxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]]},"xaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"yaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"scene":{"xaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"yaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"zaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"geo":{"bgcolor":"white","landcolor":"#E5ECF6","subunitcolor":"white","showland":true,"showlakes":true,"lakecolor":"white"},"title":{"x":0.05},"mapbox":{"style":"light"}}},"xaxis":{"anchor":"y","domain":[0.0,1.0],"title":{"text":""},"categoryorder":"array","categoryarray":["in_memory","trie","mongo","postgres_async","redis"],"type":"category"},"yaxis":{"anchor":"x","domain":[0.0,1.0],"title":{"text":"avg of vm_mbytes"}},"legend":{"title":{"text":"solution"},"tracegroupgap":0},"title":{"text":"Avg memory footprint, in mbs","font":{"size":30}},"barmode":"relative","margin":{"b":80,"l":80,"r":80,"t":100,"pad":2},"plot_bgcolor":"rgba(236, 236, 236, 0.3)","width":825}}
{{< /plotly >}}


Some highlights:
* The most consistent solution across every dimension (prefix used and number of clients) is the Trie
* Strangely, Mongo uses almost 2GB of memory and I haven't figured it out yet 🤔
* It comes as a surprise to me that with Postgres, we get very few RPS
* "hey" can't handle very well high load. Apache Benchmark is a good alternative
* Redis is amazing 🤩 its comparable with the Trie solution.



# Conclusion

Choosing the right tool for the job is important, but it's not always the most crucial factor. In many cases, the right data structure is more essential when solving complex problems.

For example, in a coding challenge, you may be tempted to use a built-in function like `reverse()` to check for a palindrome, but using a stack could be a faster and more efficient solution.

When working on software projects, it's not always necessary to choose the latest tool or framework, sometimes it's better to stick with what you know, or maybe even re-learn old solutions by going back to basics.



By the end of this post, I figure that I could use this project to test new versions of each tool, or new data structures that I might learn more about in the future.

For example, if Postgres gets bumped, or if I get the time to play with a ["Patricia Tree"](https://en.wikipedia.org/wiki/Radix_tree) (funny name), I can just implement a backend, `docker-compose up` and compare with the other solutions.

The project is self-contained enough that it allows me to expand with new solutions "as plugins" and keep the core functionality being tested.


Which I think is pretty sweet 🤓



# Resources

* Setting up grafana dashboards: https://medium.com/javarevisited/monitoring-setup-with-docker-compose-part-2-grafana-2cd2d9ff017b
* Trie data structure: https://en.wikipedia.org/wiki/Trie



👋
