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
mkdir -p monstruos

# Tipos de criatura (con orígenes donde aplica)
create_rareza_origen "monstruos/abberacion" false  # Sin orígenes, son extraplanarias
create_rareza_origen "monstruos/bestia" true      # Ej. lobos élficos
create_rareza_origen "monstruos/celestial" true   # Ej. ángeles de origen divino
create_rareza_origen "monstruos/constructo" true  # Ej. gólems enanos
create_rareza_origen "monstruos/dragon" true      # Ej. dragones élficos
create_rareza_origen "monstruos/elemental" false  # Elementales no necesitan origen
create_rareza_origen "monstruos/fatado" true      # Ej. hadas élficas
create_rareza_origen "monstruos/fiendo" true      # Ej. demonios infernales
create_rareza_origen "monstruos/gigante" true     # Ej. gigantes enanos
create_rareza_origen "monstruos/humanoide" true   # Ej. bandidos humanos
create_rareza_origen "monstruos/limo" false       # Limos no necesitan origen
create_rareza_origen "monstruos/monstruosidad" true  # Ej. quimeras infernales
create_rareza_origen "monstruos/no_muerto" true   # Ej. zombis infernales
create_rareza_origen "monstruos/planta" true      # Ej. treants élficos
create_rareza_origen "monstruos/otros" true       # Criaturas personalizadas

echo "Estructura de carpetas creada en 'monstruos/'"