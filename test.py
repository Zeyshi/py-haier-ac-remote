from haierac import HaierAC

print("-- HaierAC recv demo --")

# Change the IP address to your AC's IP address
h = HaierAC(ip="192.168.0.181", mac="18:a7:f1:6c:da:c1")
print("-- Start --")
h.recv_loop()
print("-- Hello --")
h.send_hello()
h.recv_loop()
print("-- Set target temp --")
h.set_temp(25)
h.ping()
h.recv_loop()
