import thriftpy
from thriftpy.rpc import make_client
from thriftpy.thrift import TException
from datetime import datetime

timestamp_thrift = thriftpy.load(
    'timestamp.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService


def main():
    try:
        # Instantiate a synchronous client
        client = make_client(Timestamp, '127.0.0.1', 9090)
        server_timestamp = client.getCurrentTimestamp()

        dt_object = datetime.fromtimestamp(server_timestamp)

        # Format datetime object as desired
        formatted_date = dt_object.strftime('%d/%m/%y')  # Date format: DD/MM/YY
        formatted_time = dt_object.strftime('%H:%M:%S')  # Time format: HR:MIN:SEC

        print("Date:", formatted_date)
        print("Time:", formatted_time)
    except TException as e:
        print(e)


if __name__ == '__main__':
    main()
