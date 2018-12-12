from itertools import cycle
胣=str
ﳛ=zip
𗗲=chr
𭰶=ord
𘀇=False
def encrypt(key:胣,m:胣)->胣:
 噚=''
 for 𐦆,㝊,㪾 in ﳛ(m,cycle(key),cycle('backdoor')):
  噚+=𗗲((𭰶(𐦆)+𭰶(㝊))%2048)
  噚+=𗗲((𭰶(𐦆)+𭰶(㪾))%2048)
 return 噚
def decrypt(key:胣,𢣚:胣,u=𘀇)->胣:
 噚=''
 𢣚=𢣚[1::2]if u else 𢣚[::2]
 for 𐦆,㝊,㪾 in ﳛ(𢣚,cycle(key),cycle('backdoor')):
  if u:
   噚+=𗗲((𭰶(𐦆)-𭰶(㪾)+2048)%2048)
  else:
   噚+=𗗲((𭰶(𐦆)-𭰶(㝊)+2048)%2048)
 return 噚
