from turtle import Turtle, Screen
from prettytable import PrettyTable

# timmy = Turtle()

# print(timmy)
# timmy.shape("turtle")
# timmy.color("coral")
# timmy.forward(100)

# my_screen = Screen()
# print(my_screen.canvheight)
# my_screen.exitonclick()

table = PrettyTable()

table.field_names = ["Pokemon Name", "Type"]
table.add_rows(
    [
        ["Pikachu", "Electric"], 
        ["Squirtle", "Water"]   
    ]
)

table.align = "l"

print(table)