#!/bin/bash

# Definir rarezas y orígenes
RAREZAS=(subclase

)

ORIGENES=(especializa

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
mkdir -p clases

# Clases y subclases (con orígenes donde aplica)
# Bárbaro
create_rareza_origen "clases/barbaro/berserker" true
create_rareza_origen "clases/barbaro/totem" true
create_rareza_origen "clases/barbaro/ancestros" true

# Bardo
create_rareza_origen "clases/bardo/lore" true
create_rareza_origen "clases/bardo/valor" true
create_rareza_origen "clases/bardo/espadas" true

# Clérigo
create_rareza_origen "clases/clerigo/vida" true
create_rareza_origen "clases/clerigo/guerra" true
create_rareza_origen "clases/clerigo/luz" true

# Druida
create_rareza_origen "clases/druida/luna" true
create_rareza_origen "clases/druida/tierra" true
create_rareza_origen "clases/druida/estrellas" true

# Guerrero
create_rareza_origen "clases/guerrero/campeon" true
create_rareza_origen "clases/guerrero/maestro_batalla" true
create_rareza_origen "clases/guerrero/caballero_arcano" true

# Monje
create_rareza_origen "clases/monje/sombra" true
create_rareza_origen "clases/monje/cuatro_elementos" true
create_rareza_origen "clases/monje/mano_abierta" true

# Paladín
create_rareza_origen "clases/paladin/devocion" true
create_rareza_origen "clases/paladin/venganza" true
create_rareza_origen "clases/paladin/juramento_antiguo" true

# Pícaro
create_rareza_origen "clases/picaro/ladron" true
create_rareza_origen "clases/picaro/asesino" true
create_rareza_origen "clases/picaro/arcano" true

# Explorador
create_rareza_origen "clases/explorador/cazador" true
create_rareza_origen "clases/explorador/senestre" true
create_rareza_origen "clases/explorador/amoso" true

# Hechicero
create_rareza_origen "clases/hechicero/draconic" true
create_rareza_origen "clases/hechicero" true
create_rareza_origen "alagora" true
create_rareza_origen "clases/hechicero/magia_salvaje" true
create_rareza_origen "clases/salvaje" true

# Mago
create_rareza_origen "clases/mago/abjuracion" true
create_rareza_origen "clases/mago/adivinacion" true
create_rareza_origen "clases/mago/evocacion" true

# Brujo
create_rareza_origen "clases/brujo/fiendo" true
create_rareza_origen "clases/brujo/gran_anciano" true
create_rareza_origen "clases/brujo/archifata" true

# Artificiero
create_rareza_origen "clases/artificiero/alquimista" true
create_rareza_origen "clases/artificiero/armero" true
create_rareza_origen "clases/artificiero/artillero" true

# Homebrew
create_rareza_origen "clases/homebrew/personalizadas" true

echo "Estructura de carpetas creada en 'clases/'"