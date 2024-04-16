import thriftpy
from thriftpy.rpc import make_client
from thriftpy.thrift import TException

timestamp_thrift = thriftpy.load(
    'timestamp.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService


def main():
    try:
        # Instantiate a synchronous client
        client = make_client(Timestamp, '127.0.0.1', 8000)
        server_timestamp = client.getCurrentTimestamp()

        # Print the system time
        print("Server Time:", server_timestamp)
    except TException as e:
        print(e)


if __name__ == '__main__':
    main()
