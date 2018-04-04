import grpc
import random
import asyncio
import sys

# import the generated classes
import drone_pb2
import drone_pb2_grpc


def register_client(stub):
    drone_id = stub.registerClients(drone_pb2.Droneid(id=random.randint(1, 100)))
    print("ClientID {0} registered to server".format(drone_id.id))
    return drone_id.id


def get_coordinates(stub, client_id):
    drone_id = drone_pb2.Droneid(id=client_id)
    response = drone_pb2.Coordinates
    for response1 in stub.getPosition(drone_id):
        print("[received] Moving to coordinates [{0},{1},{2}]".format(response1.x, response1.y, response1.z))


def run():
    host = '0.0.0.0'
    port = int(sys.argv[1])
    channel = grpc.insecure_channel('%s:%d' % (host, port))
    stub = drone_pb2_grpc.DronePositionStub(channel)
    drone_id = register_client(stub)
    get_coordinates(stub, drone_id)


if __name__ == '__main__':
    run()
