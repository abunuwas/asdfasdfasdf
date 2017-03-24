from configReader import ConfigReader


def api_controller_type_verifier(should_be_controller):
    def api_controller_type_verifier_decorator(f):
        def f_wrapper(self, *args, **kwargs):
            if ConfigReader.read_config_value('INSTANCETYPE', 'IsTestAPIController') != should_be_controller:
                return 'Method not supported for controller type', 400
            else:
                return f(self, *args, **kwargs)
        return f_wrapper
    return api_controller_type_verifier_decorator
