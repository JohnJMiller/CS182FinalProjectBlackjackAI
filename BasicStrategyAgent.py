'''
Basic Strategy Agent
Alice Liu, John Miller
'''

from BlackjackPlayers import Card, Hand, Player

class BasicStrategyAgent(Player):
	"""
	Agent that plays according to basic strategy.
	"""

	def __init__(self):
		self.doubledDown = False
		self.hands = [Hand([])]
		self.split = False
		self.stand = False
		
		#Fill lookup table used for selecting actions
		self.chart = {}

		self.chart[("2","2"), "2"] = "Hit"
		self.chart[("3","3"), "2"] = "Hit"
		self.chart[("4","4"), "2"] = "Hit"
		self.chart[("5","5"), "2"] = "Double Down"
		self.chart[("6","6"), "2"] = "Split"
		self.chart[("7","7"), "2"] = "Split"
		self.chart[("8","8"), "2"] = "Split"
		self.chart[("9","9"), "2"] = "Split"
		self.chart[("10","10"), "2"] = "Stand"
		self.chart[("J","J"), "2"] = "Stand"
		self.chart[("Q","Q"), "2"] = "Stand"
		self.chart[("K","K"), "2"] = "Stand"
		self.chart[("A","A"), "2"] = "Split"
		self.chart[("A","2"), "2"] = "Hit"
		self.chart[("A","3"), "2"] = "Hit"
		self.chart[("A","4"), "2"] = "Hit"
		self.chart[("A","5"), "2"] = "Hit"
		self.chart[("A","6"), "2"] = "Double Down"
		self.chart[("A","7"), "2"] = "Stand"
		self.chart[("A","8"), "2"] = "Stand"
		self.chart[("A","9"), "2"] = "Stand"

		self.chart[("2","2"), "3"] = "Split"
		self.chart[("3","3"), "3"] = "Hit"
		self.chart[("4","4"), "3"] = "Hit"
		self.chart[("5","5"), "3"] = "Double Down"
		self.chart[("6","6"), "3"] = "Split"
		self.chart[("7","7"), "3"] = "Split"
		self.chart[("8","8"), "3"] = "Split"
		self.chart[("9","9"), "3"] = "Split"
		self.chart[("10","10"), "3"] = "Stand"
		self.chart[("J","J"), "3"] = "Stand"
		self.chart[("Q","Q"), "3"] = "Stand"
		self.chart[("K","K"), "3"] = "Stand"
		self.chart[("A","A"), "3"] = "Split"
		self.chart[("A","2"), "3"] = "Hit"
		self.chart[("A","3"), "3"] = "Hit"
		self.chart[("A","4"), "3"] = "Hit"
		self.chart[("A","5"), "3"] = "Hit"
		self.chart[("A","6"), "3"] = "Double Down"
		self.chart[("A","7"), "3"] = "Double Down"
		self.chart[("A","8"), "3"] = "Stand"
		self.chart[("A","9"), "3"] = "Stand"

		self.chart[("2","2"), "4"] = "Split"
		self.chart[("3","3"), "4"] = "Split"
		self.chart[("4","4"), "4"] = "Hit"
		self.chart[("5","5"), "4"] = "Double Down"
		self.chart[("6","6"), "4"] = "Split"
		self.chart[("7","7"), "4"] = "Split"
		self.chart[("8","8"), "4"] = "Split"
		self.chart[("9","9"), "4"] = "Split"
		self.chart[("10","10"), "4"] = "Stand"
		self.chart[("J","J"), "4"] = "Stand"
		self.chart[("Q","Q"), "4"] = "Stand"
		self.chart[("K","K"), "4"] = "Stand"
		self.chart[("A","A"), "4"] = "Split"
		self.chart[("A","2"), "4"] = "Double Down"
		self.chart[("A","3"), "4"] = "Double Down"
		self.chart[("A","4"), "4"] = "Double Down"
		self.chart[("A","5"), "4"] = "Double Down"
		self.chart[("A","6"), "4"] = "Double Down"
		self.chart[("A","7"), "4"] = "Double Down"
		self.chart[("A","8"), "4"] = "Stand"
		self.chart[("A","9"), "4"] = "Stand"

		self.chart[("2","2"), "5"] = "Split"
		self.chart[("3","3"), "5"] = "Split"
		self.chart[("4","4"), "5"] = "Double Down"
		self.chart[("5","5"), "5"] = "Double Down"
		self.chart[("6","6"), "5"] = "Split"
		self.chart[("7","7"), "5"] = "Split"
		self.chart[("8","8"), "5"] = "Split"
		self.chart[("9","9"), "5"] = "Split"
		self.chart[("10","10"), "5"] = "Stand"
		self.chart[("J","J"), "5"] = "Stand"
		self.chart[("Q","Q"), "5"] = "Stand"
		self.chart[("K","K"), "5"] = "Stand"
		self.chart[("A","A"), "5"] = "Split"
		self.chart[("A","2"), "5"] = "Double Down"
		self.chart[("A","3"), "5"] = "Double Down"
		self.chart[("A","4"), "5"] = "Double Down"
		self.chart[("A","5"), "5"] = "Double Down"
		self.chart[("A","6"), "5"] = "Double Down"
		self.chart[("A","7"), "5"] = "Double Down"
		self.chart[("A","8"), "5"] = "Stand"
		self.chart[("A","9"), "5"] = "Stand"

		self.chart[("2","2"), "6"] = "Split"
		self.chart[("3","3"), "6"] = "Split"
		self.chart[("4","4"), "6"] = "Double Down"
		self.chart[("5","5"), "6"] = "Double Down"
		self.chart[("6","6"), "6"] = "Split"
		self.chart[("7","7"), "6"] = "Split"
		self.chart[("8","8"), "6"] = "Split"
		self.chart[("9","9"), "6"] = "Split"
		self.chart[("10","10"), "6"] = "Stand"
		self.chart[("J","J"), "6"] = "Stand"
		self.chart[("Q","Q"), "6"] = "Stand"
		self.chart[("K","K"), "6"] = "Stand"
		self.chart[("A","A"), "6"] = "Split"
		self.chart[("A","2"), "6"] = "Double Down"
		self.chart[("A","3"), "6"] = "Double Down"
		self.chart[("A","4"), "6"] = "Double Down"
		self.chart[("A","5"), "6"] = "Double Down"
		self.chart[("A","6"), "6"] = "Double Down"
		self.chart[("A","7"), "6"] = "Double Down"
		self.chart[("A","8"), "6"] = "Double Down"
		self.chart[("A","9"), "6"] = "Stand"

		self.chart[("2","2"), "7"] = "Split"
		self.chart[("3","3"), "7"] = "Split"
		self.chart[("4","4"), "7"] = "Hit"
		self.chart[("5","5"), "7"] = "Double Down"
		self.chart[("6","6"), "7"] = "Hit"
		self.chart[("7","7"), "7"] = "Split"
		self.chart[("8","8"), "7"] = "Split"
		self.chart[("9","9"), "7"] = "Stand"
		self.chart[("10","10"), "7"] = "Stand"
		self.chart[("J","J"), "7"] = "Stand"
		self.chart[("Q","Q"), "7"] = "Stand"
		self.chart[("K","K"), "7"] = "Stand"
		self.chart[("A","A"), "7"] = "Split"
		self.chart[("A","2"), "7"] = "Hit"
		self.chart[("A","3"), "7"] = "Hit"
		self.chart[("A","4"), "7"] = "Hit"
		self.chart[("A","5"), "7"] = "Hit"
		self.chart[("A","6"), "7"] = "Hit"
		self.chart[("A","7"), "7"] = "Stand"
		self.chart[("A","8"), "7"] = "Stand"
		self.chart[("A","9"), "7"] = "Stand"

		self.chart[("2","2"), "8"] = "Hit"
		self.chart[("3","3"), "8"] = "Hit"
		self.chart[("4","4"), "8"] = "Hit"
		self.chart[("5","5"), "8"] = "Double Down"
		self.chart[("6","6"), "8"] = "Hit"
		self.chart[("7","7"), "8"] = "Hit"
		self.chart[("8","8"), "8"] = "Split"
		self.chart[("9","9"), "8"] = "Split"
		self.chart[("10","10"), "8"] = "Stand"
		self.chart[("J","J"), "8"] = "Stand"
		self.chart[("Q","Q"), "8"] = "Stand"
		self.chart[("K","K"), "8"] = "Stand"
		self.chart[("A","A"), "8"] = "Split"
		self.chart[("A","2"), "8"] = "Hit"
		self.chart[("A","3"), "8"] = "Hit"
		self.chart[("A","4"), "8"] = "Hit"
		self.chart[("A","5"), "8"] = "Hit"
		self.chart[("A","6"), "8"] = "Hit"
		self.chart[("A","7"), "8"] = "Stand"
		self.chart[("A","8"), "8"] = "Stand"
		self.chart[("A","9"), "8"] = "Stand"

		self.chart[("2","2"), "9"] = "Hit"
		self.chart[("3","3"), "9"] = "Hit"
		self.chart[("4","4"), "9"] = "Hit"
		self.chart[("5","5"), "9"] = "Double Down"
		self.chart[("6","6"), "9"] = "Hit"
		self.chart[("7","7"), "9"] = "Hit"
		self.chart[("8","8"), "9"] = "Split"
		self.chart[("9","9"), "9"] = "Split"
		self.chart[("10","10"), "9"] = "Stand"
		self.chart[("J","J"), "9"] = "Stand"
		self.chart[("Q","Q"), "9"] = "Stand"
		self.chart[("K","K"), "9"] = "Stand"
		self.chart[("A","A"), "9"] = "Split"
		self.chart[("A","2"), "9"] = "Hit"
		self.chart[("A","3"), "9"] = "Hit"
		self.chart[("A","4"), "9"] = "Hit"
		self.chart[("A","5"), "9"] = "Hit"
		self.chart[("A","6"), "9"] = "Hit"
		self.chart[("A","7"), "9"] = "Hit"
		self.chart[("A","8"), "9"] = "Stand"
		self.chart[("A","9"), "9"] = "Stand"

		self.chart[("2","2"), "10"] = "Hit"
		self.chart[("3","3"), "10"] = "Hit"
		self.chart[("4","4"), "10"] = "Hit"
		self.chart[("5","5"), "10"] = "Hit"
		self.chart[("6","6"), "10"] = "Hit"
		self.chart[("7","7"), "10"] = "Stand"
		self.chart[("8","8"), "10"] = "Split"
		self.chart[("9","9"), "10"] = "Stand"
		self.chart[("10","10"), "10"] = "Stand"
		self.chart[("J","J"), "10"] = "Stand"
		self.chart[("Q","Q"), "10"] = "Stand"
		self.chart[("K","K"), "10"] = "Stand"
		self.chart[("A","A"), "10"] = "Split"
		self.chart[("A","2"), "10"] = "Hit"
		self.chart[("A","3"), "10"] = "Hit"
		self.chart[("A","4"), "10"] = "Hit"
		self.chart[("A","5"), "10"] = "Hit"
		self.chart[("A","6"), "10"] = "Hit"
		self.chart[("A","7"), "10"] = "Hit"
		self.chart[("A","8"), "10"] = "Stand"
		self.chart[("A","9"), "10"] = "Stand"

		self.chart[("2","2"), "10"] = "Hit"
		self.chart[("3","3"), "10"] = "Hit"
		self.chart[("4","4"), "10"] = "Hit"
		self.chart[("5","5"), "10"] = "Hit"
		self.chart[("6","6"), "10"] = "Hit"
		self.chart[("7","7"), "10"] = "Stand"
		self.chart[("8","8"), "10"] = "Split"
		self.chart[("9","9"), "10"] = "Stand"
		self.chart[("10","10"), "10"] = "Stand"
		self.chart[("J","J"), "10"] = "Stand"
		self.chart[("Q","Q"), "10"] = "Stand"
		self.chart[("K","K"), "10"] = "Stand"
		self.chart[("A","A"), "10"] = "Split"
		self.chart[("A","2"), "10"] = "Hit"
		self.chart[("A","3"), "10"] = "Hit"
		self.chart[("A","4"), "10"] = "Hit"
		self.chart[("A","5"), "10"] = "Hit"
		self.chart[("A","6"), "10"] = "Hit"
		self.chart[("A","7"), "10"] = "Hit"
		self.chart[("A","8"), "10"] = "Stand"
		self.chart[("A","9"), "10"] = "Stand"

		self.chart[("2","2"), "J"] = "Hit"
		self.chart[("3","3"), "J"] = "Hit"
		self.chart[("4","4"), "J"] = "Hit"
		self.chart[("5","5"), "J"] = "Hit"
		self.chart[("6","6"), "J"] = "Hit"
		self.chart[("7","7"), "J"] = "Stand"
		self.chart[("8","8"), "J"] = "Split"
		self.chart[("9","9"), "J"] = "Stand"
		self.chart[("10","10"), "J"] = "Stand"
		self.chart[("J","J"), "J"] = "Stand"
		self.chart[("Q","Q"), "J"] = "Stand"
		self.chart[("K","K"), "J"] = "Stand"
		self.chart[("A","A"), "J"] = "Split"
		self.chart[("A","2"), "J"] = "Hit"
		self.chart[("A","3"), "J"] = "Hit"
		self.chart[("A","4"), "J"] = "Hit"
		self.chart[("A","5"), "J"] = "Hit"
		self.chart[("A","6"), "J"] = "Hit"
		self.chart[("A","7"), "J"] = "Hit"
		self.chart[("A","8"), "J"] = "Stand"
		self.chart[("A","9"), "J"] = "Stand"

		self.chart[("2","2"), "Q"] = "Hit"
		self.chart[("3","3"), "Q"] = "Hit"
		self.chart[("4","4"), "Q"] = "Hit"
		self.chart[("5","5"), "Q"] = "Hit"
		self.chart[("6","6"), "Q"] = "Hit"
		self.chart[("7","7"), "Q"] = "Stand"
		self.chart[("8","8"), "Q"] = "Split"
		self.chart[("9","9"), "Q"] = "Stand"
		self.chart[("10","10"), "Q"] = "Stand"
		self.chart[("J","J"), "Q"] = "Stand"
		self.chart[("Q","Q"), "Q"] = "Stand"
		self.chart[("K","K"), "Q"] = "Stand"
		self.chart[("A","A"), "Q"] = "Split"
		self.chart[("A","2"), "Q"] = "Hit"
		self.chart[("A","3"), "Q"] = "Hit"
		self.chart[("A","4"), "Q"] = "Hit"
		self.chart[("A","5"), "Q"] = "Hit"
		self.chart[("A","6"), "Q"] = "Hit"
		self.chart[("A","7"), "Q"] = "Hit"
		self.chart[("A","8"), "Q"] = "Stand"
		self.chart[("A","9"), "Q"] = "Stand"

		self.chart[("2","2"), "K"] = "Hit"
		self.chart[("3","3"), "K"] = "Hit"
		self.chart[("4","4"), "K"] = "Hit"
		self.chart[("5","5"), "K"] = "Hit"
		self.chart[("6","6"), "K"] = "Hit"
		self.chart[("7","7"), "K"] = "Stand"
		self.chart[("8","8"), "K"] = "Split"
		self.chart[("9","9"), "K"] = "Stand"
		self.chart[("10","10"), "K"] = "Stand"
		self.chart[("J","J"), "K"] = "Stand"
		self.chart[("Q","Q"), "K"] = "Stand"
		self.chart[("K","K"), "K"] = "Stand"
		self.chart[("A","A"), "K"] = "Split"
		self.chart[("A","2"), "K"] = "Hit"
		self.chart[("A","3"), "K"] = "Hit"
		self.chart[("A","4"), "K"] = "Hit"
		self.chart[("A","5"), "K"] = "Hit"
		self.chart[("A","6"), "K"] = "Hit"
		self.chart[("A","7"), "K"] = "Hit"
		self.chart[("A","8"), "K"] = "Stand"
		self.chart[("A","9"), "K"] = "Stand"

		self.chart[("2","2"), "A"] = "Hit"
		self.chart[("3","3"), "A"] = "Hit"
		self.chart[("4","4"), "A"] = "Hit"
		self.chart[("5","5"), "A"] = "Hit"
		self.chart[("6","6"), "A"] = "Hit"
		self.chart[("7","7"), "A"] = "Hit"
		self.chart[("8","8"), "A"] = "Split"
		self.chart[("9","9"), "A"] = "Stand"
		self.chart[("10","10"), "A"] = "Stand"
		self.chart[("J","J"), "A"] = "Stand"
		self.chart[("Q","Q"), "A"] = "Stand"
		self.chart[("K","K"), "A"] = "Stand"
		self.chart[("A","A"), "A"] = "Split"
		self.chart[("A","2"), "A"] = "Hit"
		self.chart[("A","3"), "A"] = "Hit"
		self.chart[("A","4"), "A"] = "Hit"
		self.chart[("A","5"), "A"] = "Hit"
		self.chart[("A","6"), "A"] = "Hit"
		self.chart[("A","7"), "A"] = "Stand"
		self.chart[("A","8"), "A"] = "Stand"
		self.chart[("A","9"), "A"] = "Stand"

		# fill second lookup table used for selecting actions that first table didn't catch

		self.chart2 = {}

		self.chart2[5, "2"] = "Hit"
		self.chart2[6, "2"] = "Hit"
		self.chart2[7, "2"] = "Hit"
		self.chart2[8, "2"] = "Hit"
		self.chart2[9, "2"] = "Double Down"
		self.chart2[10, "2"] = "Double Down"
		self.chart2[11, "2"] = "Double Down"
		self.chart2[12, "2"] = "Hit"
		self.chart2[13, "2"] = "Stand"
		self.chart2[14, "2"] = "Stand"
		self.chart2[15, "2"] = "Stand"
		self.chart2[16, "2"] = "Stand"
		self.chart2[17, "2"] = "Stand"

		self.chart2[5, "3"] = "Hit"
		self.chart2[6, "3"] = "Hit"
		self.chart2[7, "3"] = "Hit"
		self.chart2[8, "3"] = "Hit"
		self.chart2[9, "3"] = "Double Down"
		self.chart2[10, "3"] = "Double Down"
		self.chart2[11, "3"] = "Double Down"
		self.chart2[12, "3"] = "Hit"
		self.chart2[13, "3"] = "Stand"
		self.chart2[14, "3"] = "Stand"
		self.chart2[15, "3"] = "Stand"
		self.chart2[16, "3"] = "Stand"
		self.chart2[17, "3"] = "Stand"

		self.chart2[5, "4"] = "Hit"
		self.chart2[6, "4"] = "Hit"
		self.chart2[7, "4"] = "Hit"
		self.chart2[8, "4"] = "Hit"
		self.chart2[9, "4"] = "Double Down"
		self.chart2[10, "4"] = "Double Down"
		self.chart2[11, "4"] = "Double Down"
		self.chart2[12, "4"] = "Stand"
		self.chart2[13, "4"] = "Stand"
		self.chart2[14, "4"] = "Stand"
		self.chart2[15, "4"] = "Stand"
		self.chart2[16, "4"] = "Stand"
		self.chart2[17, "4"] = "Stand"

		self.chart2[5, "5"] = "Hit"
		self.chart2[6, "5"] = "Hit"
		self.chart2[7, "5"] = "Hit"
		self.chart2[8, "5"] = "Double Down"
		self.chart2[9, "5"] = "Double Down"
		self.chart2[10, "5"] = "Double Down"
		self.chart2[11, "5"] = "Double Down"
		self.chart2[12, "5"] = "Stand"
		self.chart2[13, "5"] = "Stand"
		self.chart2[14, "5"] = "Stand"
		self.chart2[15, "5"] = "Stand"
		self.chart2[16, "5"] = "Stand"
		self.chart2[17, "5"] = "Stand"

		self.chart2[5, "6"] = "Hit"
		self.chart2[6, "6"] = "Hit"
		self.chart2[7, "6"] = "Hit"
		self.chart2[8, "6"] = "Double Down"
		self.chart2[9, "6"] = "Double Down"
		self.chart2[10, "6"] = "Double Down"
		self.chart2[11, "6"] = "Double Down"
		self.chart2[12, "6"] = "Stand"
		self.chart2[13, "6"] = "Stand"
		self.chart2[14, "6"] = "Stand"
		self.chart2[15, "6"] = "Stand"
		self.chart2[16, "6"] = "Stand"
		self.chart2[17, "6"] = "Stand"

		self.chart2[5, "7"] = "Hit"
		self.chart2[6, "7"] = "Hit"
		self.chart2[7, "7"] = "Hit"
		self.chart2[8, "7"] = "Hit"
		self.chart2[9, "7"] = "Hit"
		self.chart2[10, "7"] = "Double Down"
		self.chart2[11, "7"] = "Double Down"
		self.chart2[12, "7"] = "Hit"
		self.chart2[13, "7"] = "Hit"
		self.chart2[14, "7"] = "Hit"
		self.chart2[15, "7"] = "Hit"
		self.chart2[16, "7"] = "Hit"
		self.chart2[17, "7"] = "Stand"

		self.chart2[5, "8"] = "Hit"
		self.chart2[6, "8"] = "Hit"
		self.chart2[7, "8"] = "Hit"
		self.chart2[8, "8"] = "Hit"
		self.chart2[9, "8"] = "Hit"
		self.chart2[10, "8"] = "Double Down"
		self.chart2[11, "8"] = "Double Down"
		self.chart2[12, "8"] = "Hit"
		self.chart2[13, "8"] = "Hit"
		self.chart2[14, "8"] = "Hit"
		self.chart2[15, "8"] = "Hit"
		self.chart2[16, "8"] = "Hit"
		self.chart2[17, "8"] = "Stand"

		self.chart2[5, "9"] = "Hit"
		self.chart2[6, "9"] = "Hit"
		self.chart2[7, "9"] = "Hit"
		self.chart2[8, "9"] = "Hit"
		self.chart2[9, "9"] = "Hit"
		self.chart2[10, "9"] = "Double Down"
		self.chart2[11, "9"] = "Double Down"
		self.chart2[12, "9"] = "Hit"
		self.chart2[13, "9"] = "Hit"
		self.chart2[14, "9"] = "Hit"
		self.chart2[15, "9"] = "Hit"
		self.chart2[16, "9"] = "Hit"
		self.chart2[17, "9"] = "Stand"

		self.chart2[5, "10"] = "Hit"
		self.chart2[6, "10"] = "Hit"
		self.chart2[7, "10"] = "Hit"
		self.chart2[8, "10"] = "Hit"
		self.chart2[9, "10"] = "Hit"
		self.chart2[10, "10"] = "Hit"
		self.chart2[11, "10"] = "Double Down"
		self.chart2[12, "10"] = "Hit"
		self.chart2[13, "10"] = "Hit"
		self.chart2[14, "10"] = "Hit"
		self.chart2[15, "10"] = "Hit"
		self.chart2[16, "10"] = "Hit"
		self.chart2[17, "10"] = "Stand"

		self.chart2[5, "J"] = "Hit"
		self.chart2[6, "J"] = "Hit"
		self.chart2[7, "J"] = "Hit"
		self.chart2[8, "J"] = "Hit"
		self.chart2[9, "J"] = "Hit"
		self.chart2[10, "J"] = "Hit"
		self.chart2[11, "J"] = "Double Down"
		self.chart2[12, "J"] = "Hit"
		self.chart2[13, "J"] = "Hit"
		self.chart2[14, "J"] = "Hit"
		self.chart2[15, "J"] = "Hit"
		self.chart2[16, "J"] = "Hit"
		self.chart2[17, "J"] = "Stand"

		self.chart2[5, "Q"] = "Hit"
		self.chart2[6, "Q"] = "Hit"
		self.chart2[7, "Q"] = "Hit"
		self.chart2[8, "Q"] = "Hit"
		self.chart2[9, "Q"] = "Hit"
		self.chart2[10, "Q"] = "Hit"
		self.chart2[11, "Q"] = "Double Down"
		self.chart2[12, "Q"] = "Hit"
		self.chart2[13, "Q"] = "Hit"
		self.chart2[14, "Q"] = "Hit"
		self.chart2[15, "Q"] = "Hit"
		self.chart2[16, "Q"] = "Hit"
		self.chart2[17, "Q"] = "Stand"

		self.chart2[5, "K"] = "Hit"
		self.chart2[6, "K"] = "Hit"
		self.chart2[7, "K"] = "Hit"
		self.chart2[8, "K"] = "Hit"
		self.chart2[9, "K"] = "Hit"
		self.chart2[10, "K"] = "Hit"
		self.chart2[11, "K"] = "Double Down"
		self.chart2[12, "K"] = "Hit"
		self.chart2[13, "K"] = "Hit"
		self.chart2[14, "K"] = "Hit"
		self.chart2[15, "K"] = "Hit"
		self.chart2[16, "K"] = "Hit"
		self.chart2[17, "K"] = "Stand"

		self.chart2[5, "A"] = "Hit"
		self.chart2[6, "A"] = "Hit"
		self.chart2[7, "A"] = "Hit"
		self.chart2[8, "A"] = "Hit"
		self.chart2[9, "A"] = "Hit"
		self.chart2[10, "A"] = "Hit"
		self.chart2[11, "A"] = "Double Down"
		self.chart2[12, "A"] = "Hit"
		self.chart2[13, "A"] = "Hit"
		self.chart2[14, "A"] = "Hit"
		self.chart2[15, "A"] = "Hit"
		self.chart2[16, "A"] = "Hit"
		self.chart2[17, "A"] = "Stand"


	def getCharts(self):
		"""
		returns the lookup tables (used for the HMM)
		"""
		
		return (self.chart, self.chart2)


	def getLegalThings(self, state, inGame):
		"""
		returns list of legal actions
		"""
		return self.getLegalActions()

	def getAction(self, state, hand_index,inGame):
		"""
		Chooses an action for the agent
		"""
		
		hand = self.hands[hand_index]
		if len(hand.getCards()) == 2:

			string_hand = (hand.getCards()[0].getName(), hand.getCards()[1].getName())
			string_hand_rev = (hand.getCards()[1].getName(), hand.getCards()[0].getName())

			# for hands in chart 1
			if (string_hand, state["Upcard"].getName()) in self.chart:
				# check if a legal action, then return action
				if self.chart[(string_hand, state["Upcard"].getName())] in self.getLegalThings(state, inGame):
					return self.chart[(string_hand, state["Upcard"].getName())]
			elif (string_hand_rev, state["Upcard"]) in self.chart:
				# check if a legal action, then return action
				if self.chart[(string_hand_rev, state["Upcard"].getName())] in self.getLegalThings(state, inGame):
					return self.chart[(string_hand_rev, state["Upcard"].getName())]

			# for hands in chart 2
			else:
				# face cards count as 10
				upcard = state["Upcard"].getName() 
				if upcard == "K" or upcard == "Q" or upcard == "J":
					upcard = "10"
				# 17 and over values are counted the same
				if hand.getValue() >= 17:
					if (17, upcard) in self.chart2:
						# check if legal action
						if self.chart2[17, upcard] in self.getLegalThings(state, inGame):
							return self.chart2[17, upcard]
				# check if new value, upcard pair in chart 2
				if (state["Hand"][hand_index].getValue(), upcard) in self.chart2:
					if self.chart2[state["Hand"][hand_index].getValue(), upcard] in self.getLegalThings(state,inGame):
						return self.chart2[state["Hand"].getValue(), upcard]

				# catchall--should never be used
				else:
					return "Stand"

		# if more than 2 cards in hand, default to checking in chart 2
		else:
			upcard = state["Upcard"].getName() 
			# as before, face cards count as 10
			if upcard == "K" or upcard == "Q" or upcard == "J":
				upcard = "10"
			# 17 and over values are counted the same
			if hand.getValue() >= 17:
				if (17, upcard) in self.chart2:
					if self.chart2[17, upcard] in self.getLegalThings(state, inGame):
						return self.chart2[17, upcard]
			# check if new value, upcard pair in chart 2
			if (state["Hand"][hand_index].getValue(), upcard) in self.chart2:
				if self.chart2[state["Hand"][hand_index].getValue(), upcard] in self.getLegalThings(state,inGame):
					return self.chart2[state["Hand"].getValue(), upcard]

			# catchall--should never be used
			else:
				return "Stand"


		



