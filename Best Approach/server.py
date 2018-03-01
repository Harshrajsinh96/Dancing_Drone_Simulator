from concurrent import futures
import time
import grpc
import drone_pb2
import drone_pb2_grpc
import sys
from client import _CLIENT_PORT

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_SERVER_PORT = '3000'

class RegisterDrone(drone_pb2_grpc.DroneSimulationServicer):
    drone_list = []
    x = 0; y = 0; z = 0
    delta_x = 0; delta_y = 0; delta_z = 0
    ask_for_new_cords = False

    def registerDrone(self, request, context):
        drone_id = request.droneId
        new_cords = None
        if drone_id not in self.drone_list:
            self.drone_list.append(drone_id)
            new_cords = get_and_update_cords()
            RegisterDrone.ask_for_new_cords = True
        return drone_pb2.RegisterResponse(droneId=request.droneId, cords=new_cords)

def send_cord_updates(input_cords):
    channel = grpc.insecure_channel('localhost:'+ _CLIENT_PORT)
    stub = drone_pb2_grpc.DroneSimulationStub(channel)

    if input_cords:
        RegisterDrone.x = int(input_cords[0])
        RegisterDrone.y = int(input_cords[1])
        RegisterDrone.z = int(input_cords[2])

    for drone_id in RegisterDrone.drone_list:
        stub.updateOnCords(drone_pb2.UpdateCordsRequest(droneId=drone_id, cords=get_and_update_cords()))

def get_and_update_cords():
    ret_cords = "[" + str(RegisterDrone.x) + "," + str(RegisterDrone.y) + "," + str(RegisterDrone.z) + "]"
    update_cords()
    return ret_cords

def update_cords():
    RegisterDrone.x = RegisterDrone.x + RegisterDrone.delta_x
    RegisterDrone.y = RegisterDrone.y + RegisterDrone.delta_y
    RegisterDrone.z = RegisterDrone.z + RegisterDrone.delta_z

def serve(initial_cords, cords_delta):

    # set initial cords
    RegisterDrone.x = int(initial_cords[0])
    RegisterDrone.y = int(initial_cords[1])
    RegisterDrone.z = int(initial_cords[2])

    # set cords delta
    RegisterDrone.delta_x = int(cords_delta[0])
    RegisterDrone.delta_y = int(cords_delta[1])
    RegisterDrone.delta_z = int(cords_delta[2])

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    drone_pb2_grpc.add_DroneSimulationServicer_to_server(RegisterDrone(), server)
    server.add_insecure_port('[::]:'+_SERVER_PORT)
    server.start()
    print("Server started at " + _SERVER_PORT+".")

    while True:
        if RegisterDrone.ask_for_new_cords:
            input_cord = input("Enter New Co-Ordinates[X,Y,Z]: ")
            print("------------------------------------")
            input_cord = input_cord.split(",")
            in_list = []
            for i in input_cord:
                in_list.append(i)
            send_cord_updates(in_list)

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    initial_cords = sys.argv[1].split(",")
    cords_delta = sys.argv[2].split(",")
    serve(initial_cords, cords_delta)