from bitdeli.chain import Profiles

def test(profiles):
	for profile in profiles:
		pass
	yield {'head': '42'}

Profiles().map(test).show('text')
