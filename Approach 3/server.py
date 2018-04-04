import grpc
from concurrent import futures
import time
import sys
import threading

import drone_pb2
import drone_pb2_grpc

counter_id = 0
coordinate_list1 = [sys.argv[1]]
coordinate_list2 = []
p, q, r = sys.argv[2].split(',')
coordinate_list2.append(p + "," + q + "," + r)


class CoordinatesProvider(drone_pb2_grpc.DronePositionServicer):

    def registerClients(self, request, context):
        global counter_id
        counter_id += 1
        response = drone_pb2.Droneid(id=counter_id)
        return response

    def getPosition(self, request, context):
        while True:
            if request.id == 1:
                if not coordinate_list1 and not coordinate_list2:
                    coor = input("Enter the new coordinates [x,y,z]:")
                    coordinate_list1.append(coor)
                    x, y, z = coordinate_list1[0].split(',')
                    coordinate_list2.append(str(int(x) + 10) + "," + y + "," + z)

            if request.id == 1:
                for coordinate in coordinate_list1:
                    x, y, z = coordinate.split(',')
                    yield drone_pb2.Coordinates(x=int(x), y=int(y), z=int(z))
                    coordinate_list1.pop()

            elif request.id == 2:
                for coordinate in coordinate_list2:
                    x, y, z = coordinate.split(',')
                    yield drone_pb2.Coordinates(x=int(x), y=int(y), z=int(z))
                    coordinate_list2.pop()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), maximum_concurrent_rpcs=50)
    drone_pb2_grpc.add_DronePositionServicer_to_server(CoordinatesProvider(), server)
    print('Starting server. Listening on port 3000.')
    host = '127.0.0.1'
    port = 3000
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
