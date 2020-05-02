import matplotlib.pyplot as plt
import numpy as np


# Throughput vs Latency

x = np.arange(0, 1001, 100)
y = [356685.224171002,12786.6163222628,12029.273820611,12362.9193561736,13954.6115386983,12609.3512813668,14541.1975376845,14927.2723218222,9287.62425829736,11087.8281205675,4707.29393232289]


plt.figure()
plt.plot(x[1:], y[1:])
plt.xlabel("Network latency (ms)")
plt.ylabel("Throughput (Bytes/sec)")
plt.title("Throughput vs latency/delay")
plt.savefig("plots/latency_graph.png")
# plt.show()

# Throughput vs packet loss

x = [5, 15, 35 ,50, 65, 90]
y = [4018.34871333816, 2498.41825837277,1267.3672967858, 239.061976438694, 432.219011490783, 24.2234138625971]


plt.figure()
# plt.bar(x, y)
plt.plot(x, y)
plt.xlabel("Packet Loss %")
plt.ylabel("Throughput (Bytes/sec)")
plt.title("Throughput vs Packet loss")
plt.savefig("plots/packet_loss_graph.png")
# plt.show()

# Throughput vs Packet corruption %

x = [5, 15, 25, 35, 50, 65, 75]
y = [4713.92167265316,1827.98328414253,1547.95918265218,1003.79923199577,654.631667456492,411.402785206851,201.098504868917]


plt.figure()
# plt.bar(x, y)
plt.plot(x, y)
plt.xlabel("Packet corruption %")
plt.ylabel("Throughput (Bytes/sec)")
plt.title("Throughput vs Packet corruption %")
plt.savefig("plots/packet_corruption_graph.png")
# plt.show()