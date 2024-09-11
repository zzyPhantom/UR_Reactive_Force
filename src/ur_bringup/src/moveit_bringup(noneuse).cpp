#include "rclcpp/rclcpp.hpp"
#include "moveit/planning_interface/planning_interface.h"
#include "moveit/robot_state/robot_state.h"
#include "moveit/planning_scene/planning_scene.h"
#include "moveit/planning_scene_interface/planning_scene_interface.h"
#include "sensor_msgs/msg/joint_state.hpp"
#include "std_msgs/msg/string.hpp"

class MoveIt2Node : public rclcpp::Node
{
public:
  MoveIt2Node() : Node("moveit2_node")
  {
    // Initialize the RobotModelLoader and RobotState
    moveit::core::RobotModelPtr robot_model;
    robot_model = moveit::core::RobotModel::loadURDF("path/to/model.urdf");
    robot_state_ = std::make_shared<moveit::core::RobotState>(robot_model_);

    // Initialize the PlanningSceneInterface
    planning_scene_interface_ = std::make_shared<moveit::planning_interface::PlanningSceneInterface>();

    // Create subscription
    joint_states_sub_ = this->create_subscription<sensor_msgs::msg::JointState>(
      "/joint_states", 10, std::bind(&MoveIt2Node::jointStatesCallback, this, std::placeholders::_1));
  }

private:
  void jointStatesCallback(const sensor_msgs::msg::JointState::SharedPtr msg)
  {
    // Update the RobotState with received joint states
    robot_state_->setVariablePositions(msg->name, msg->position);

    // Update the PlanningSceneInterface with your changes, if needed
    // For example, you might add/update objects in the scene
    // planning_scene_interface_->applyCollisionObjects(...);
  }

  rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr joint_states_sub_;
  std::shared_ptr<moveit::core::RobotModelLoader> robot_model_loader_;
  moveit::core::RobotModelConstPtr robot_model_;
  std::shared_ptr<moveit::core::RobotState> robot_state_;
  std::shared_ptr<moveit::planning_interface::PlanningSceneInterface> planning_scene_interface_;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MoveIt2Node>());
  rclcpp::shutdown();
  return 0;
}