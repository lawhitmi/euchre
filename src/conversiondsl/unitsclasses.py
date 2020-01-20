class FeetAndInches(object):

    def __init__(self, feet, inches=0, fraction_inches=0):

        self._feetDecimal = feet + inches / 12 + fraction_inches / 12
        a = self.breakDown()
        self._feet = a[0]
        self._inches = a[1]
        self._fraction_inches = a[2]

    @property
    def feetDecimal(self):
        return self._feetDecimal

    @property
    def feet(self):
        return self._feet

    @property
    def inches(self):
        return self._inches

    @property
    def fraction_inches(self):
        return self._fraction_inches

    def breakDown(self):
        feet = int(self.feetDecimal)
        inches = int((self.feetDecimal - feet) * 12)
        fracInches = int((((self.feetDecimal - feet) * 12) - inches) * 32)

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
        return self._feet + self._inches / 12 + (self._fraction_inches[0] / self._fraction_inches[1]) / 12

    def __add__(self, y):
        return FeetAndInches(self.feetDecimal + y.feetDecimal)

    def __sub__(self, y):
        return FeetAndInches(self.feetDecimal - y.feetDecimal)

    def __str__(self):
        response = str(self._feet) + "' "
        if self._inches != 0:
            response += str(self._inches)
        if self._fraction_inches[0] != 0:
            response += ' ' + str(self._fraction_inches[0]) + '/' + \
                        str(self._fraction_inches[1])
        if self._inches != 0 or self._fraction_inches[0] != 0:
            response += '"'
        return response

