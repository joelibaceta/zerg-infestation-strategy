En este ejemplo evita el conocido Zergling Rush poder disponer de una duración mas prolongada de la partida, presenciar algunas interesantes batallas y el efecto de los algoritmos

> No se está usando alguna estrategia de aprendizaje por reforzamiento ya que el objetivo es tener una primera aproximación con el API de Starcraft II

## Estrategia usada:

1. Mantener un nivel optimo de obreros por Hatchery y todos correctamente distribuidos trabajanado.
2. Mantener los Overlords en constante exploracion para tener una vision general del mapa.
3. Dar la orden de atacar cada vez que se cumplan las siguientes condiciones:
  - Se cuenta con 50 Zerglins en espera
  - Se cuenta con varios Zerglings y 10 Hidraliscos en espera.
4. Investigar el Boost Metabolic para mejorar el ataque de los Zerglings.
5. Construir overlords cada vez que sea necesario.
6. Desarrollar el arbol de tecnologias lo mas rapido posible para construir Zerglings.
7. Desarrollar el arbol de tecnologias lo mas rapido posible para construir Hidraliscos.
8. Construir expaciones eligiendo aleatoriamente algun lugar optimo para una base nueva.
9. Construir una Reina (`Queen`) por cada base y usar la habilidad `Inject Larva` para mejorar la produccion de larvas.

## ¿Cómo Funciona?

Starcraft2 disponibiliza un API para poder interactuar y ejecutar acciones en el juego a travez de un bot, para este caso hice uno en particular para la raza Zerg (Mi favorita).

Para interactuar con el API de SC2 usando Python, debemos instalar el paquete sc2 y descargar algun mapa. (Incluyo uno en el repo).

Con esto ya podemos empezar a escribir algun script basico, el siguiente inicia el juego carga el bot el mapa y define un nombre para guardar el replay.

```python
def main():
    sc2.run_game(sc2.maps.get("AutomatonLE"), [
        Bot(Race.Zerg, ZergInfestationStrategyBot()),
        Computer(Race.Terran, Difficulty.Hard)
    ], realtime=False, save_replay_as="ZvT.SC2Replay")

if __name__ == '__main__':
    main()
```

> ZergInfestationStrategyBot es la clase que contiene la logica del Bot

Luego es necesario incluir en el loop del juego las ordenes que vamos a ir ejecutando.

```python
class ZergInfestationStrategyBot(sc2.BotAI):
    async def on_step(self, iteration):
        # Ejecutar acciones en cada iteracion
```

### Construir, distribuir trabajadores y producir recursos

![build-and-work](/images/BuildAndWork.png)

Por ejemplo para construir y distribuir en posiciones de trabajo los Drones usamos el siguiente snippet

```python
class ZergInfestationStrategyBot(sc2.BotAI):

    def __init__(self):
        self.extractors = 0
    
    async def on_step(self, iteration):
        await self.build_and_distribute_workers()
    
    async def build_and_distribute_workers(self):
        await self.distribute_workers()
        
        if self.hq.assigned_harvesters < self.hq.ideal_harvesters:
            if self.can_afford(DRONE) and self.larvae.amount > 0:
                await self.do(self.larvae.random.train(DRONE))

        if self.extractors == 0:
            drone = self.workers.random
            target = self.state.vespene_geyser.closest_to(drone.position)
            err = await self.do(drone.build(EXTRACTOR, target))
            if not err:
                self.extractors += 1

        if self.extractors < self.units(HATCHERY).amount and self.units(LAIR).ready.exists:
            if self.can_afford(EXTRACTOR) and self.workers.exists:
                drone = self.workers.random
                target = self.state.vespene_geyser.closest_to(drone.position)
                err = await self.do(drone.build(EXTRACTOR, target))
                if not err:
                    self.extractors += 1
```

Aqui le decimos al Bot que empiece distribuyendo los trabajadores, posteriormente valide si el numero de trabajadores es menor al optimo necesario en ese caso si hay larvas disponibles construir uno.

Adicionalmente se valida si el contador de extractores es 0 para construir el primero lo mas rapido posible y los siguientes poco antes de poder construir Hidraliscos para no penalizar los recursos tan pronto.

Se controla que el numero de extractores sea unicamente 1 por base.


#### Construir y distribuir trabajadores