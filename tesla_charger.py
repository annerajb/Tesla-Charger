#!/usr/bin/python3
import can
from threading import Timer,Thread,Event
import time
interface = "vcan0"

bus = can.interface.Bus(interface, bustype='socketcan_native')

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
			acvolts = recv_message.data[1]
			ac_present = recv_message.data[2] & 12;
			mod_end = recv_message.data[2] & 0x40;
			mod_flt = recv_message.data[2] & 0x20;
			accur = (recv_message.data[6] & 3) << 7) + (recv_message.data[5] & 0x7f)
			print("Phase(%d) ac volt: %f current: %f "% (phase, ,accur))
			
		elif message_id == 0x210:
			print("{0:b}".format(recv_message.data[0], '016b'))
		elif message_id == 0x220:
			dc_current = ((recv_message.data[5] << 8) + recv_message.data[4]) * 0.000839233
			dc_voltage = ((recv_message.data[3] << 8) + recv_message.data[2]) * 0.01052864
			print("Phase(%d) DC voltage: %0.2f V current: %0.2f mA" % (phase, dc_voltage/100,dc_current/1000 ))
		elif message_id == 0x230:
			//temperature message 1
			print("Phase(%d) temp 0: %0.2f" %(recv_message.data[0]-40));
			print("Phase(%d) temp 1: %0.2f" %(recv_message.data[1]-40));
			print("Phase(%d) inlet temp: %0.2f" %(recv_message.data[5]-40));
		elif message_id == 0x240:
			//current temperature limit message
			print("Phase(%d) temp limit: %0.2f" %(recv_message.data[0]*0.234375));
		elif message_id == 0x540:
			print("Phase(%d) error count %d of 50"%(phase,recv_message.data[0]))
	else:
		print("new sender ID save this capture!!!!!!!!!!1")


if "__main__" == __name__:
	stopflag = Event()
	thread = MyThread(stopflag,bus)
	#thread.start()

	#run_scheduled_task(bus)

	while True:
		recv_message = bus.recv();
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

