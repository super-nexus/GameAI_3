
class BaseLLMAgent():

    def determine_region(self, image_path):
        raise NotImplementedError("This method must be implemented by the subclass")

    def name(self):
        raise NotImplementedError("This method must be implemented by the subclass")
