class classtest:
	data = 2
	def debug(self,d):
		return 'debug'
		
	def debug2(self,t):
		print 'debug2'
		
	@classmethod
	def debug3(cls,t):
		cls.data = t

print classtest.data

cla = classtest()
cla.data = 4
t = cla.debug('d')
cla.debug3(5)
print cla.data
print classtest.data
print t
cla.debug2('ttt')

print cla.data

classtest.data = 3
classtest.debug3(9)

print classtest.data
print cla.data

dic = {}
dec = { 'tt':3,'dd': 'tt'}
print dec
print ', '.join(['%s' %t for t in dec])
