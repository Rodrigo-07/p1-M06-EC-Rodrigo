# Inicializar comunicação no cmd_vel do Turtlesim X
# Criar estrutura de fila (deque)
# Poder enviar comandos pela CLI
# Mandar argumentos pela execução da CLI

# Comandos: vx vy vtheta tempo_em_ms

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from collections import deque
# import typer


import time


def cli(args=None):
    # Inicilizar o RCLPY
    rclpy.init(args=args)


    movTurtle = MovTurtle()

    print("Coloque o movimentos desejados para a movimentação do turtlesim")
    print("Siga o padrão: vx vy vtheta tempo_em_ms")

    while True:
        new_moviment = input("Coloque o movimento desejado ")

        movTurtle.mov_dq.append(new_moviment)

        movTurtle.mov_deque_manager()

    # O spin do TurtleControler serve para manter o programa rodando até que seja finalizado
    # rclpy.spin(movTurtle)

    # # Limpar os nós
    # movTurtle.destroy_node()
    # rclpy.shutdown()

class MovTurtle(Node):
    # Inicializar a classe
    def __init__(self):
        # Chamar o construtor da classe Node
        super().__init__('mov_turtle')
        # Criar um objeto do tipo Publisher, que publica no tópico /turtle1/cmd_vel
        self.publisher_mov = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # Instanciando um deque vazio

        self.mov_dq = deque()

    def move_turtle(self, vx, vy, theta):
        # Criar mensagem tipo Twist
        msg = Twist()

        msg.linear.x = float(vx)
        msg.linear.y = float(vy)
        
        msg.angular.z = float(theta)
        
        # Publicar a mensagem
        self.publisher_mov.publish(msg)
        self.get_logger().info(f'Tartaruga movida para {vx}, {vy}, {theta}')

        return True
    
    # Movimentar a tartaruga por um tempo
    def mov_direction_timer(self, vx, vy, theta, tempo):
        tempo = float(tempo)
        tempo = tempo/1000

        while tempo > 0:
            self.move_turtle(vx, vy, theta)

            time.sleep(1)

            tempo -= 1
            self.get_logger().info('Duração: ' + str(tempo))
        
            self.stop_movement()
    
    def mov_deque_manager(self):

        while len(self.mov_dq) > 0:
            # print(f"Deque: {self.mov_dq}")

            moviment = self.mov_dq[0]
            moviment = moviment.split()

            print(moviment)

            self.mov_direction_timer(moviment[0], moviment[1], moviment[2], moviment[3])
            
            self.mov_dq.popleft()


            time.sleep(1)
        
        print(f"Deque: {self.mov_dq}")
    
    # Parar tartaruga
    def stop_movement(self):
        msg = Twist()
        self.publisher_mov.publish(msg)
        self.get_logger().info('Tartaruga parada')


def main(args=None):

    cli()


if __name__ == "__main__":
    main()
