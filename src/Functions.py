class Function:
    def call(self, func_name, args):
        to_call = getattr(self, func_name, self.generic_call)
        return to_call(args)

    def generic_call(self, function):
        raise Exception("Error: function called '{}' not defined.".format("UNKOWN"))

    def sqrt(self, args):
        value = args[0]

        return value**(1/2)