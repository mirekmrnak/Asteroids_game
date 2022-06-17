objects = [1, True, "ahoj"]
classes_in_game = set()

for object in objects:
        classes_in_game.add(type(object))
        
print(classes_in_game)
print(float in classes_in_game)