#!/usr/bin/python3
import can
from threading import Timer,Thread,Event
import time
interface = "vcan0"

bus = can.interface.Bus(interface, bustype='socketcan_native')
known_ids = {0x10C:0,0x207:0,0x20B:0,0x209:0,0x36b:0, 0x237:0, 0x717:0, 0x34b:0, 0x217:0, 0x219:0,0x21b:0, 0x71b:0,0x227:0,0x229:0, 0x22b:0, 0x719:0, 0x349:0, 0x327:0, 0x367:0, 0x337:0,0x339:0, 0x23b:0, 0x43c:0, 0x549:0, 0x239:0, 0x547:0, 0x249:0, 0x24b:0, 0x44c:0, 0x32b:0, 0x42c:0, 0x357:0, 0x359:0, 0x35b:0, 0x45c:0, 0x33b:0, 0x5e7:0,0x5e9:0, 0x247:0,0x5eb:0, 0x329:0, 0x369:0, 0x347:0, 0x377:0, 0x379:0, 0x54b:0, 0x37b:0}
found_ids = {}

def send_trigger(bus_):
        msg = can.Message(arbitration_id=0x411,
                      data=[    0x31, 0x00,0x80],
                      extended_id=False)
        bus_.send(msg)

class MyThread(Thread):
	def __init__(self,event,_bus):
		Thread.__init__(self)
		self.stopped=event
		self._bus = _bus
	def run(self):
		while not self.stopped.wait(1):
			send_trigger(self._bus)
		


#def run_scheduled_task(bus):
#    timer = Timer(1, send_trigger, [bus])
#    timer.start()

def phase_message(recv_message,sender_id,message_id,phase):
	if False:
		return
	if sender_id == 0x7 or sender_id == 0x9 or sender_id == 0xB:
	#       print("message_id: 0x%x sender_id: 0x%x" % (message_id, sender_id))
		if message_id == 0x200:
			print("Phase(%d) ac volt: %f current: %f "% (phase, recv_message.data[1],((((recv_message.data[7] & 3) * 256) + recv_message.data[6]))/28))
			asd22 = None
		elif message_id == 0x220:
			dc_voltage = (recv_message.data[3] * 256) + recv_message.data[2]
			dc_current = (recv_message.data[7] * 256) + recv_message.data[6]
			print("Phase(%d) dc voltage: %0.2f V current: %0.2f mA" % (phase, dc_voltage/100,dc_current/1000 ))
		elif message_id == 0x540:
			print("Phase(%d) error count %d of 50"%(phase,recv_message.data[0]))
		elif message_id == 0x500:
			print("Phase(%d) unique message so far only seen when phases are alone.")
	else:
		print("new sender ID save this capture!!!!!!!!!!1")


if "__main__" == __name__:
	stopflag = Event()
	thread = MyThread(stopflag,bus)
	#thread.start()

	#run_scheduled_task(bus)

	while True:
		recv_message = bus.recv(15);
		if recv_message is None:
			print("no new messages after 15 seconds")
			for key, value in found_ids.items():
				if key not in known_ids:
					print("new key: 0x%x" %(key));
			break
		found_ids[recv_message.arbitration_id] =1 #found_ids[recv_message.arbitration_id] + 1

		sender_id =  recv_message.arbitration_id & 0xF 
		message_id = recv_message.arbitration_id & 0xFFF0

		#determine who was the sender
		if sender_id == 0x7:
			phase_message(recv_message,sender_id,message_id,1)
		elif sender_id == 0x9:
			phase_message(recv_message,sender_id,message_id,2)
		elif sender_id == 0xB:
			phase_message(recv_message,sender_id,message_id,3)
		elif sender_id == 0xC:
			#message from control
			#print("dc current setpoint")
			if message_id == 0x450:
				print("Control DC voltage: %0.2f feedback: %0.2f" % ((recv_message.data[7] * 256 + recv_message.data[6])/100,(recv_message.data[1]*256 + recv_message.data[0])/100))
				
			elif message_id == 0x420:
				print("Control DC current: %0.2f " % ((recv_message.data[3] * 256 + recv_message.data[2])/100))
			elif message_id == 0x100:
				print("Control Board error count %d of 50"%(recv_message.data[0]))
		else:	
			print("new message sender!!!!!!!!!!!! save this capture!!!!")			

