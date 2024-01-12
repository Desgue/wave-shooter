
class SceneManager:
    def __init__(self, scene):
        self.scene = scene
        self.go_to(self.scene)
    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self