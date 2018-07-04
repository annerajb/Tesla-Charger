#!/usr/bin/python3
import threading
import can
from threading import Timer,Thread,Event
import time
interface = "vcan0"
bus = can.interface.Bus(interface, bustype='socketcan_native')
class ChargerController():
	voltset = 0
	curset = 0
	curreq = 0
	currampt = 500
	curramp = 0
	setting = 1
	incomingByte = 0
	tlast = 0
	test52 = 0x15
	test53 = 0x0e
	debug = 1
	test20 = 0x42
	test21 = 0x60
	test24 = 0x64
	def charger_msgs(self,bus_):
		print("sending periodic")
		msg = can.Message(arbitration_id=0x45C,data=[self.voltset&0xF,self.voltset & 0xF0, self.test52,self.test53,0x00,0x00,0x90,0x8c],extended_id=False)
		bus_.send(msg)
		msg = can.Message(arbitration_id=0x42C,data=[self.test20,self.test21,self.curreq&0xF,self.curreq & 0xF0,self.test24,0x00,0x00,0x00],extended_id=False)
		bus_.send(msg)
		msg = can.Message(arbitration_id=0x368,data=[0x03,0x49,0x29,0x11,0x00,0x0c,0x40,0xff],extended_id=False)
		bus_.send(msg)
		self.run_scheduled_task(bus_)

	def run_scheduled_task(self,bus):
	    timer = Timer(.100, self.charger_msgs, [bus])
	    timer.start()
	def candecode(self,message):
		if can.arbitration_id == 0x207:
			acvolt = message.data[1]
			accur = ((message.data[8]& 0x3)*256+message.data[7])
			newframe = newframe | 2
		elif can.arbitration_id == 0x227:
			dccur = message.data[7]*256+message.data[6]
			dcvolt = message.data[3]*256+message.data[2]
			newframe = newframe | 2
		else:
			return
	def collect_input(self,):
		state = False
		while True:
			try:
				msg = input()
				if msg == 'v':
					voltset = int(input()) * 100
					setting = 1
				elif msg == 't':
					currampt = int(input())
					setting = 1
				elif msg == 's':
					state = not state 
					setting = 1
				elif msg == 'c':
					curset = int(input()) * 1500
					setting = 1
				else:
					print("v for voltage setting")
					print("t for current ramp time")
					print("s for start and stop")
					print("c for current in whole numbers")
					continue
				if setting == 1:
					if state == True:
						print("charger on")
					else:
						print("charger off")
					print("Set Voltage: %d V"%(voltset * 0.01))
					print("Set Current: %d A" %(curset * 0.00066666))
					print("Set Ramptime: %d ms" %(currampt))
					curramp = ((curset-curreq)/500)
					print("Ramp Current: % A"%(curramp))
					setting = 0
				if state == False:
					test52 = 0x15
					test53 = 0x0e
					test21 = 0x60
					test24 = 0x64
				elif state == True:
					test52 = 0x14
					test53 = 0x02e
					test21 =0xc4
					test24 = 0xfe
				if curreq != curset:
					if (((time.time()*1000.0)-tlast)>1):
						tlast = time.time()*1000.0
						curreq = curreq + curramp
				if debug != 0:
					print(time.time()*1000.0)
					print("Charger Feedback // AC Voltage: ")
					print(acvolt)
					print("AC Current: ")
					print(accur/28)
					print("DC voltage:")
					print(dcvolt / 100 )
					print(dccur/1000)
				
			except ValueError:
				print("invalid command")
				print("v for voltage setting")
				print("t for current ramp time")
				print("s for start and stop")
				print("c for current in whole numbers")
				continue				
	def process(self,bus):
		stopflag = Event()
		#thread = MyThread(stopflag,bus)
		#thread.start()
		t = threading.Thread(target=self.collect_input)
		t.start()
		self.run_scheduled_task(bus)

		while True:
			recv_message = bus.recv();
			if recv_message is None:
				print("no new messages after 15 seconds")
				for key, value in found_ids.items():
					if key not in known_ids:
						print("new key: 0x%x" %(key));
				break

			sender_id =  recv_message.arbitration_id & 0xF 
			message_id = recv_message.arbitration_id & 0xFFF0
			self.candecode(recv_message)	
if "__main__" == __name__:
	ChargerController().process(bus)
