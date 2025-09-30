# TP-Link TD-W8961N Telnet Client

This project is a Python-based Telnet client designed to interact with TP-Link TD-W8961N routers to fetch and display real-time status, ADSL rate, and line quality information.

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/oshliaer/tp-link-td-w8961n-telnet-client
    cd tp-link-td-w8961n-telnet-client
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a `.env` file in the root of the project with the following variables:

```text
ROUTER_IP=192.168.1.1
ROUTER_PASSWORD=admin
POLLING_INTERVAL_SECONDS=60
```

## Usage

(To be added in a later step - how to run the script)
