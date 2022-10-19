#!/usr/bin/env python3
class color:
	GREEN = '\033[1;32;48m'
	YELLOW = '\033[1;33;48m'
	RED = '\033[1;31;48m'
	END = '\033[1;37;0m'

class HotBeverage:
	def __init__(self, price=None, name=None) -> None:
		self.price = 0.30 if price is None else price
		self.name = "hot beverage" if name is None else name

	def __str__(self) -> str:
		DESCRIPTION = ("name : {name}\nprice : {price}\ndescription : {description}")
		return DESCRIPTION.format(name=self.name, price=self.price, description=color.GREEN+self.description()+color.END)

	def description(self) -> str:
		return "Just some hot water in a cup."

class Coffee(HotBeverage):
	def __init__(self) -> None:
		super().__init__(0.40, "coffee")

	def description(self) -> str:
		return "A coffee, to stay awake."

class Tea(HotBeverage):
	def __init__(self) -> None:
		super().__init__(0.30, "tea")

	def description(self) -> str:
		return "Just some hot water in a cup."

class Chocolate(HotBeverage):
	def __init__(self) -> None:
		super().__init__(0.50, "chocolate")

	def description(self) -> str:
		return "Chocolate, sweet chocolate..."

class Cappuccino(HotBeverage):
	def __init__(self) -> None:
		super().__init__(0.45, "cappuccino")

	def description(self) -> str:
		return "Un po' di Italia nella sua tazza!"
