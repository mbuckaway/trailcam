#
#
# Standard location for all customer errors/exceptions

class ConfigError(RuntimeError):
   def __init__(self, section):
      self.section = section

class DeviceError(RuntimeError):
   def __init__(self, devicePath):
      self.device = str(devicePath)

class InvalidFunctionError(RuntimeError):
   def __init__(self, function):
      self.function = str(function)
