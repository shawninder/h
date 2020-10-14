from newrelic.agent import data_source_generator, register_data_source

from h.streamer.streamer import WORK_QUEUE
from h.streamer.websocket import WebSocket

PREFIX = "Custom/WebSocket"


@data_source_generator(name="WebSocket Metrics")
def websocket_metrics():
    """
    Report metrics about the websocket service to New Relic.

    See https://docs.newrelic.com/docs/agents/python-agent/supported-features/python-custom-metrics.
    """

    connections_active = len(WebSocket.instances)
    connections_anonymous = sum(
        1 for ws in WebSocket.instances if not ws.authenticated_userid
    )

    # Allow us to tell the difference between reporting 0 and not reporting
    yield f"{PREFIX}/Alive", 1

    yield f"{PREFIX}/Connections/Active", connections_active
    yield f"{PREFIX}/Connections/Authenticated", connections_active - connections_anonymous
    yield f"{PREFIX}/Connections/Anonymous", connections_anonymous

    yield f"{PREFIX}/WorkQueueSize", WORK_QUEUE.qsize()


def includeme(_config):  # pragma: no cover
    register_data_source(websocket_metrics)
