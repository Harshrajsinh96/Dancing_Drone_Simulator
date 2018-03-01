from __future__ import print_function
from concurrent import futures
import time
import grpc
import sys
import drone_pb2
import drone_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_CLIENT_PORT = '3001'

def run(port):
    channel = grpc.insecure_channel('localhost:%d'%port)
    stub = drone_pb2_grpc.DroneSimulationStub(channel)
    for i in range(2):
        response = stub.registerDrone(drone_pb2.RegisterRequest(droneId=str(get_random_id())))
        print("Client id [" + response.droneId + "] connected to the server.")
        print("Cords received, moving to " + response.cords)
        i += 1
    print("----------------------------------------------")
        
def get_random_id():
    from random import randint
    return randint(1000, 9999)

class GetCordUpdate(drone_pb2_grpc.DroneSimulationServicer):

	def updateOnCords(self, request, context):
		print("Cords Updated, Drone [" + request.droneId + "] moving to " + request.cords)
		return drone_pb2.UpdateCordsResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    drone_pb2_grpc.add_DroneSimulationServicer_to_server(GetCordUpdate(), server)
    server.add_insecure_port('[::]:'+_CLIENT_PORT)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    port = int(sys.argv[1])
    run(port)
    serve()