
def writer(output_pipe, server_id):
    while True:
        data = output_pipe.recv()

        if data == None: break

        print data
