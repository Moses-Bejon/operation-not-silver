from math import ceil

class railFence():

    def __init__(self, cipher):
        self.__cipher = cipher
        self.__length = len(self.__cipher)

    def plainTexts(self):

        for rails in range(2,self.__length):

            self.__period = 2*(rails-1)

            for offset in range(self.__period):

                yield self.decipher(rails,offset)

    def getPositionOfCharacter(self,offset,railLengths):
        localOffset = offset%self.__period
        if localOffset > self.__period/2:
            rail = self.__period-localOffset
        else:
            rail = localOffset

        if rail == 0:
            totalLength = 0
        else:
            totalLength = railLengths[rail-1]


        totalLength += self.__distanceCoveredAlongRails[rail]
        self.__distanceCoveredAlongRails[rail] += 1

        return totalLength

    def decipher(self,rails,offset):

        finalOffset = (offset + self.__length - 1) % self.__period

        topLength = ceil((self.__length-(self.__period-offset)) / self.__period)

        defaultLength = 2 * topLength
        lengths = [topLength]

        for rail in range(1,rails-1):
            length= defaultLength
            if offset <= rail:
                length += 2
            elif offset <= self.__period-rail:
                length += 1
            if finalOffset < rail:
                length -= 2
            elif finalOffset < self.__period-rail:
                length -= 1

            lengths.append(length+lengths[-1])

        bottomLength = topLength
        if finalOffset < rails-1:
            bottomLength -= 1
        if offset <= rails:
            bottomLength += 1
        lengths.append(bottomLength+lengths[-1])

        plainText = []
        self.__distanceCoveredAlongRails = [0] * rails
        for character in range(self.__length):
            position = self.getPositionOfCharacter(offset+character,lengths)
            plainText.append(self.__cipher[position])

        return plainText