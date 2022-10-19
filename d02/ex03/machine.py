#!/usr/bin/env python3
import random
from beverages import HotBeverage, Coffee, Tea, Chocolate, Cappuccino, color

class CoffeeMachine:
	class EmptyCup(HotBeverage):
		def __init__(self) -> None:
			super().__init__(0.90, "empty cup")
		
		def description(self) -> str:
			return color.YELLOW + "An empty cup?! Gimme my money back!" + color.END

	class BrokenMachineException(Exception):
		def __init__(self, message="This coffee machine has to be repaired."):
			self.message = color.RED + message + color.END
			super().__init__(self.message)

	def __init__(self) -> None:
		self.broken = 10

	def repair(self) -> None:
		self.broken = 10

	def serve(self, drink: HotBeverage) -> HotBeverage():
		if (self.broken <= 0):
			raise CoffeeMachine.BrokenMachineException
		self.broken -= 1
		if random.randint(0,5) == 0:
			return CoffeeMachine.EmptyCup()
		return drink()

def main():
	coffee_machine = CoffeeMachine()
	for _ in range(22):
		try:
			print (coffee_machine.serve(random.choice([Coffee, Tea, Chocolate, Cappuccino])))
		except CoffeeMachine.BrokenMachineException as e:
			print (e)
			coffee_machine.repair()

if __name__ == "__main__":
	main()