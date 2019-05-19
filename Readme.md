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