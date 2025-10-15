from rclpy.lifecycle import LifecycleNode, TransitionCallbackReturn, State
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import torch

class VLMBaseLifecycleNode(LifecycleNode):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.bridge = CvBridge()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.rgb_image = None

    def on_configure(self, state: State):
        try:
            self.model = self.load_model()
            if self.model:
                self.get_logger().info("Model loaded successfully.")
                return TransitionCallbackReturn.SUCCESS
            else:
                self.get_logger().error("Model loading failed.")
                return TransitionCallbackReturn.FAILURE
        except Exception as e:
            self.get_logger().error(f"Configuration failed: {e}")
            return TransitionCallbackReturn.FAILURE

    def on_activate(self, state: State):
        try:
            self.create_services()
            return TransitionCallbackReturn.SUCCESS
        except Exception as e:
            self.get_logger().error(f"Activation failed: {e}")
            return TransitionCallbackReturn.FAILURE

    def on_deactivate(self, state: State):
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state: State):
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, state: State):
        return TransitionCallbackReturn.SUCCESS

    # Diese Methoden implementieren Kindklassen:
    def load_model(self):
        raise NotImplementedError

    def create_services(self):
        raise NotImplementedError
