import rclpy
from rclpy.node import Node
from moveit_commander import RobotCommander, PlanningSceneInterface, MoveGroupCommander
from moveit_commander import RobotCommander, PlanningSceneInterface
from sensor_msgs.msg import JointState
from moveit_msgs.msg import PlanningScene
from std_msgs.msg import Header

class MoveItNode(Node):
    def __init__(self):
        super().__init__('moveit_node')

        # Initialize MoveIt commander
        moveit_commander.roscpp_initialize(sys.argv)
        
        # Create MoveIt RobotCommander and PlanningSceneInterface
        self.robot = RobotCommander()
        self.scene = PlanningSceneInterface()
        
        # Set up subscribers to joint_states and robot_state_publisher
        self.joint_states_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_states_callback,
            10
        )
        
        self.robot_state_publisher_sub = self.create_subscription(
            PlanningScene,
            '/move_group/monitored_planning_scene',
            self.robot_state_publisher_callback,
            10
        )
        
        self.joint_states = None
        self.robot_state = None

        # Add initial objects to the planning scene if needed
        self.add_initial_objects_to_scene()

    def joint_states_callback(self, msg):
        self.joint_states = msg
        # You can process joint states here and update the PlanningScene if necessary

    def robot_state_publisher_callback(self, msg):
        self.robot_state = msg
        # Update the PlanningScene with the robot state

    def add_initial_objects_to_scene(self):
        # Example: Add a box to the planning scene
        self.scene.add_box("box", pose=[0.5, 0.5, 0.5], size=(0.1, 0.1, 0.1))

def main(args=None):
    rclpy.init(args=args)

    moveit_node = MoveItNode()
    
    rclpy.spin(moveit_node)
    
    moveit_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()