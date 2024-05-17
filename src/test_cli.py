import typer
import rclpy
from rclpy.node import Node
from InquirerPy.resolver import prompt
from InquirerPy.utils import InquirerPyKeybindings
from geometry_msgs.msg import Twist, Vector3
import time

# from classes.robot import TurtleBot

app = typer.Typer()

def show_menu():
    questions = [
        {
            'type': 'list',
            'name': 'action',
            'message': 'What do you want to do?',
            'choices': ['front', 'back', 'left', 'right', 'exit', 'stop'],
        },
    ]

    keybindings: InquirerPyKeybindings = {
        "interrupt": [{"key": "q"}, {"key": "c-c"}],
    }

    try:
        return prompt(questions, keybindings=keybindings)['action']
    except KeyboardInterrupt:
        return 'panic'

def main():
    rclpy.init(args=None)
    robot = TurtleBot()

    print(
"""
Se em qualquer momento você desejar parar o robô, pressione 'Q'.
"""
    )
    while True:
        action = show_menu()
        match action:
            case 'front':
                print("Mover para frente")
                robot.move_forward(0.1, 1.0)
            case 'back':
                print("Mover para trás")
                robot.move_backward(0.1, 1.0)
            case 'left':
                print("Mover para a esquerda")
                robot.rotate_left(2.0, 1.0)
            case 'right':
                print("Mover para a direita")
                robot.rotate_right(2.0, 1.0)
            case 'stop':
                print("Parada de emergência")
                robot.emergency_stop()
            case 'panic':
                print("Parada de emergência")
                robot.emergency_stop()
                robot.destroy_node()
                rclpy.shutdown()
                exit()
            case 'exit':
                robot.destroy_node()
                rclpy.shutdown()
                exit()

if __name__ == "__main__":
    main()
