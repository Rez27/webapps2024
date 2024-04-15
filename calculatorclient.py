import thriftpy
from thriftpy.rpc import make_client
from thriftpy.thrift import TException

timestamp_thrift = thriftpy.load(
    'timestamp.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService


def main():
    try:
        # Instantiate a synchronous client
        client = make_client(Timestamp, '127.0.0.1', 9090)
        client_timestamp = datetime.now().timestamp()  # Get current timestamp in seconds

    # Use the stub method to call the RPC Server. This is a blocking call.
        server_timestamp = client.echoTimestamp(client_timestamp)

        # Print the system time
        print("System Time:", server_timestamp)
    except TException as e:
        print(e)


if __name__ == '__main__':
    main()
