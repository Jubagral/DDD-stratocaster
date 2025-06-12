#!/bin/bash

# Definir rarezas y orígenes
RAREZAS=(
  "muy_comun"
  "comun"
  "poco_comun"
  "raro"
  "muy_raro"
  "legendario"
)

ORIGENES=(
  "elfico"
  "enano"
  "humano"
  "infernal"
  "otro"
)

# Función para crear subcarpetas de rareza y origen
create_rareza_origen() {
  local base_path=$1
  local use_origen=$2  # true/false para incluir orígenes
  for rareza in "${RAREZAS[@]}"; do
    if [ "$use_origen" = true ]; then
      for origen in "${ORIGENES[@]}"; do
        mkdir -p "${base_path}/${rareza}/${origen}"
      done
    else
      mkdir -p "${base_path}/${rareza}"
    fi
  done
}

# Crear estructura de carpetas
mkdir -p items

# Armas (con orígenes)
create_rareza_origen "items/armas/espadas" true
create_rareza_origen "items/armas/arcos" true
create_rareza_origen "items/armas/hachas" true
create_rareza_origen "items/armas/dagas" true
create_rareza_origen "items/armas/bastones" true
create_rareza_origen "items/armas/lanzas" true
create_rareza_origen "items/armas/mazas" true
create_rareza_origen "items/armas/otros" true

# Armaduras (con orígenes)
create_rareza_origen "items/armaduras/ligeras" true
create_rareza_origen "items/armaduras/medias" true
create_rareza_origen "items/armaduras/pesadas" true
create_rareza_origen "items/armaduras/escudos" true
create_rareza_origen "items/armaduras/vestimentas" true
create_rareza_origen "items/armaduras/accesorios_defensivos" true

# Pociones (sin orígenes)
create_rareza_origen "items/pociones/curativas" false
create_rareza_origen "items/pociones/ofensivas" false
create_rareza_origen "items/pociones/defensivas" false
create_rareza_origen "items/pociones/soporte" false
create_rareza_origen "items/pociones/venenos" false
create_rareza_origen "items/pociones/raras" false
create_rareza_origen "items/pociones/legendarias" false

# Anillos (con orígenes)
create_rareza_origen "items/anillos" true

# Amuletos (con orígenes)
create_rareza_origen "items/amuletos" true

# Reliquias (con orígenes)
create_rareza_origen "items/reliquias/divinas" true
create_rareza_origen "items/reliquias/profanas" true
create_rareza_origen "items/reliquias/unicidad" true

# Herramientas (sin orígenes)
create_rareza_origen "items/herramientas/herreria" false
create_rareza_origen "items/herramientas/alquimia" false
create_rareza_origen "items/herramientas/ladron" false
create_rareza_origen "items/herramientas/curacion" false
create_rareza_origen "items/herramientas/exploracion" false
create_rareza_origen "items/herramientas/artesania" false

# Libros (con orígenes)
create_rareza_origen "items/libros/conjuros" true
create_rareza_origen "items/libros/manuales" true
create_rareza_origen "items/libros/historia" true
create_rareza_origen "items/libros/bestias" true
create_rareza_origen "items/libros/grimorios" true
create_rareza_origen "items/libros/malditos" true

# Materiales (sin orígenes)
create_rareza_origen "items/materiales/metales" false
create_rareza_origen "items/materiales/gemas" false
create_rareza_origen "items/materiales/organicos" false
create_rareza_origen "items/materiales/vegetales" false
create_rareza_origen "items/materiales/elementales" false
create_rareza_origen "items/materiales/etereos" false

# Vehículos (con orígenes)
create_rareza_origen "items/vehiculos/monturas" true
create_rareza_origen "items/vehiculos/carromatos" true
create_rareza_origen "items/vehiculos/barcos" true
create_rareza_origen "items/vehiculos/voladores" true
create_rareza_origen "items/vehiculos/aereonaves" true
create_rareza_origen "items/vehiculos/planarios" true

# Contenedores (sin orígenes)
create_rareza_origen "items/contenedores/bolsas" false
create_rareza_origen "items/contenedores/cofres" false
create_rareza_origen "items/contenedores/mochilas" false
create_rareza_origen "items/contenedores/dimensionales" false

# Instrumentos (con orígenes)
create_rareza_origen "items/instrumentos/musicales" true
create_rareza_origen "items/instrumentos/rituales" true
create_rareza_origen "items/instrumentos/mecanicos" true
create_rareza_origen "items/instrumentos/magicos" true

# Componentes (sin orígenes)
create_rareza_origen "items/componentes/hechiceria" false
create_rareza_origen "items/componentes/invocacion" false
create_rareza_origen "items/componentes/transmutacion" false
create_rareza_origen "items/componentes/necromancia" false
create_rareza_origen "items/componentes/divinacion" false
create_rareza_origen "items/componentes/alquimia" false
create_rareza_origen "items/componentes/genericos" false
create_rareza_origen "items/componentes/elementales" false

# Esferas mágicas (sin orígenes)
create_rareza_origen "items/esferas_magicas" false

# Objetos inteligentes (con orígenes)
create_rareza_origen "items/objetos_inteligentes" true

# Otros (sin orígenes)
create_rareza_origen "items/otros/experimental" false
create_rareza_origen "items/otros/curiosos" false

echo "Estructura de carpetas creada en 'items/'"