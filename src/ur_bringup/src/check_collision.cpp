#include <rclcpp/rclcpp.hpp>
#include <moveit_msgs/srv/get_state_validity.hpp>
#include <moveit_msgs/msg/robot_state.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/robot_state/conversions.h>

class StateValidityChecker : public rclcpp::Node
{
public:
  StateValidityChecker() : Node("state_validity_checker")
  {
    // Create a client for the GetStateValidity service
    client_ = this->create_client<moveit_msgs::srv::GetStateValidity>("check_state_validity");

    // Ensure the service is available
    while (!client_->wait_for_service(std::chrono::seconds(10)))
    {
      if (!rclcpp::ok())
      {
        RCLCPP_ERROR(this->get_logger(), "Interrupted while waiting for the service. Exiting.");
        return;
      }
      RCLCPP_INFO(this->get_logger(), "Service not available. Waiting again...");
    }

    // Create a MoveGroupInterface instance
    auto node = this->shared_from_this();  // Use shared pointer to the node
    moveit::planning_interface::MoveGroupInterface move_group(node, "arm");

    // Get the current robot state
    moveit::core::RobotStatePtr current_state = move_group.getCurrentState();

    // Set new joint angles
    std::vector<double> joint_angles = {0.1, -0.2, 0.3, -0.4, 0.5, -0.6};
    move_group.setJointValueTarget(joint_angles);
    current_state->setJointGroupPositions(move_group.getCurrentState()->getJointModelGroup("arm"), joint_angles);

    // Convert RobotState to RobotStateMsg
    moveit_msgs::msg::RobotState state_msg;
    moveit::core::robotStateToRobotStateMsg(*current_state, state_msg);

    // Create a request
    auto request = std::make_shared<moveit_msgs::srv::GetStateValidity::Request>();
    request->robot_state = state_msg;

    // Send the request
    auto result_future = client_->async_send_request(request);

    // Wait for the result
    if (rclcpp::spin_until_future_complete(this->get_node_base_interface(), result_future) == rclcpp::FutureReturnCode::SUCCESS)
    {
      auto result = result_future.get();
      if (result->valid)
      {
        RCLCPP_INFO(this->get_logger(), "The state is valid.");
      }
      else
      {
        RCLCPP_INFO(this->get_logger(), "The state is invalid.");
      }
    }
    else
    {
      RCLCPP_ERROR(this->get_logger(), "Failed to call service GetStateValidity.");
    }
  }

private:
  rclcpp::Client<moveit_msgs::srv::GetStateValidity>::SharedPtr client_;
};

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<StateValidityChecker>();
  rclcpp::shutdown();
  return 0;
}