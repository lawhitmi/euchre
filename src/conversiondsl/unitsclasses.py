# TODO Ensure this class is immutable
class FeetAndInches(object):

    def __init__(self, feet, inches=0, fraction_inches=0):

        if fraction_inches != 0:
            self.feetDecimal = feet + inches / 12 + fraction_inches / 12

        else:
            self.feetDecimal = feet + inches / 12

        a = self.breakDown()
        self.feet = a[0]
        self.inches = a[1]
        self.fraction_inches = a[2]

    def breakDown(self):
        feet = int(self.getDecimal())
        inches = int((self.getDecimal() - feet) * 12)
        fracInches = int((((self.getDecimal() - feet) * 12) - inches) * 32)

        result = ()
        if fracInches == 0:
            result = (0, 0)
        else:
            for i in range(4, -1, -1):
                if fracInches % 2 ** i == 0:
                    result = (int(fracInches / 2 ** i), int(32 / 2 ** i))
                    break
                elif i == 0:
                    result = (int(fracInches), int(32))
        return [feet, inches, result]

    def convertToDecimal(self):
        return self.feet + self.inches / 12 + (self.fraction_inches[0] / self.fraction_inches[1]) / 12

    def getDecimal(self):
        return self.feetDecimal

    def __add__(self, y):
        return FeetAndInches(self.getDecimal() + y.getDecimal())

    def __sub__(self, y):
        return FeetAndInches(self.getDecimal() - y.getDecimal())

    def __str__(self):
        response = str(self.feet) + "' "
        if self.inches != 0:
            response += str(self.inches)
        if self.fraction_inches[0] != 0:
            response += ' ' + str(self.fraction_inches[0]) + '/' + \
                        str(self.fraction_inches[1])
        if self.inches != 0 or self.fraction_inches[0] != 0:
            response += '"'
        return response

