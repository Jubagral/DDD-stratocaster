# Update Adventure Dictionary Script

Este script (`update_adventure_dictionary_dynamic.py`) es una herramienta para **Donde Duermen los Dados**, diseñada para gestionar y actualizar un diccionario de entidades de **D&D 5e 2024** en el archivo `llibrerys/adventu_dic.json`. Recorre recursivamente la carpeta `llibrerys/`, procesa archivos JSON que contienen entidades como ítems, monstruos, conjuros, PNJs, localizaciones, y tipos personalizados (ej. vehículos, monturas), y genera un diccionario centralizado para su uso en la creación de infoproductos y aventuras.

## Características

- **Procesamiento dinámico**: Detecta y clasifica entidades según su campo `type` (ej. `item`, `monster`, `vehiculo`), creando categorías nuevas automáticamente.
- **Manejo de múltiples entidades**: Extrae subentidades (ej. PNJs e ítems en aventuras) y las añade individualmente.
- **Eliminación de obsoletos**: Excluye entidades cuyos JSONs ya no existan.
- **Optimización para carpetas grandes**: Usa indexación de rutas para reducir lecturas innecesarias.
- **Modo exhaustivo**: Con el flag `--force`, revisa todos los JSONs para detectar cambios.
- **Validación estricta**: Asegura que las entidades tengan `type`, `id`, y `name`.
- **Detección de colisiones**: Reporta IDs duplicados entre JSONs.
- **Exclusión de carpetas**: Permite ignorar carpetas como `backups` o `temp`.
- **Registro de acciones**: Genera un log opcional con detalles de procesamiento.
- **Soporte de codificaciones**: Maneja JSONs en UTF-8 y Latin-1.

## Requisitos

- **Python**: Versión 3.6 o superior.
- **Módulos estándar**: `os`, `json`, `pathlib`, `argparse`, `time`, `logging`.
- **Estructura de carpetas**: Una carpeta `llibrerys/` con JSONs organizados (ej. `llibrerys/items/`, `llibrerys/aventuras/`).
- **Formato de JSONs**: Cada entidad debe tener al menos `type`, `id`, y `name`. Ejemplo:
  ```json
  {
    "type": "item",
    "id": "ITEM001",
    "name": "Espada de Sombraluz",
    "description": "Una espada élfica.",
    "origen": "elfico",
    "rareza": "raro"
  }
  ```

## Instalación

1. Guarda el script como `update_adventure_dictionary_dynamic.py` en el directorio raíz de tu proyecto (donde está `llibrerys/`).
2. Asegúrate de que Python esté instalado:
   ```bash
   python --version
   ```
3. No se requieren dependencias externas; usa los módulos estándar de Python.

## Uso

Ejecuta el script desde la línea de comandos. El diccionario se genera o actualiza en `llibrerys/adventu_dic.json`.

### Comandos Básicos

- **Ejecución estándar**:
  ```bash
  python update_adventure_dictionary_dynamic.py
  ```
  Procesa solo JSONs nuevos o modificados, optimizando para carpetas grandes.

- **Modo exhaustivo** (revisa todos los JSONs):
  ```bash
  python update_adventure_dictionary_dynamic.py --force
  ```
  Útil si has modificado JSONs existentes.

- **Rutas personalizadas**:
  ```bash
  python update_adventure_dictionary_dynamic.py /custom/path /custom/adventu_dic.json
  ```

- **Excluir carpetas**:
  ```bash
  python update_adventure_dictionary_dynamic.py --exclude backups temp
  ```

- **Generar log**:
  ```bash
  python update_adventure_dictionary_dynamic.py --log update.log
  ```

- **Combinado**:
  ```bash
  python update_adventure_dictionary_dynamic.py --force --exclude backups --log update.log
  ```

### Opciones

| Opción | Alias | Descripción |
|--------|-------|-------------|
| `root_path` | | Carpeta raíz (default: `llibrerys`). |
| `output_file` | | Archivo de salida (default: `llibrerys/adventu_dic.json`). |
| `--force` | `-f` | Procesa todos los JSONs, incluso si no han cambiado. |
| `--exclude` | | Lista de carpetas a excluir (ej. `backups temp`). |
| `--log` | | Archivo de log para registrar acciones. |

### Salida

- **Archivo**: `adventu_dic.json` con categorías como `items`, `monstruos`, `pnjs`, etc. Ejemplo:
  ```json
  {
    "items": [
      {
        "id": "ITEM001",
        "name": "Espada de Sombraluz",
        "type": "item",
        "path": "/absolute/path/llibrerys/items/ITEM001.json",
        "description": "Una espada élfica.",
        "origen": "elfico",
        "rareza": "raro"
      }
    ],
    "monturas": [
      {
        "id": "MOUNT001",
        "name": "Caballo de Guerra",
        "type": "montura",
        "path": "/absolute/path/llibrerys/monturas/MOUNT001.json",
        "description": "Caballo de combate.",
        "origen": "humano"
      }
    ]
  }
  ```

- **Consola**: Reporte de procesamiento:
  ```plaintext
  2025-06-12 18:59:00 - INFO - Diccionario actualizado en llibrerys/adventu_dic.json
  2025-06-12 18:59:00 - INFO - Entidades procesadas: 42
  2025-06-12 18:59:00 - INFO - Archivos procesados: 15
  2025-06-12 18:59:00 - INFO - Tiempo de ejecución: 2.35 segundos
  2025-06-12 18:59:00 - INFO - Modo force: desactivado
  ```

- **Log** (si se usa `--log`): Detalles de colisiones, errores, y advertencias.

## Estructura de Carpetas

Organiza los JSONs en `llibrerys/` según el tipo de entidad. Ejemplo:
```
llibrerys/
├── items/
│   └── armas/espadas/raro/elfico/ITEM001.json
├── monstruos/
│   └── humanoide/comun/humano/MON002.json
├── aventuras/
│   └── intriga/nivel_1_4/humano/ADV002.json
└── monturas/
    └── comun/humano/MOUNT001.json
```

Los JSONs de aventuras pueden contener subentidades (ej. PNJs, ítems):
```json
{
  "type": "adventure",
  "id": "ADV002",
  "name": "Sombras en Piedraluna",
  "pnjs": [
    {
      "id": "PNJ002",
      "name": "Mara la Susurradora",
      "description": "Líder del culto.",
      "role": "antagonista"
    }
  ],
  "items": [
    {
      "id": "ITEM003",
      "name": "Anillo de Protección",
      "description": "+1 a la CA.",
      "rareza": "poco_comun"
    }
  ]
}
```

## Notas

- **Validación**: Las entidades deben tener `type`, `id`, y `name`. Las subentidades (ej. PNJs en aventuras) no necesitan `type`.
- **Colisiones**: Si un `id` aparece en múltiples JSONs para la misma categoría, se mantiene la primera y se reporta una advertencia.
- **Codificación**: Soporta UTF-8 y Latin-1. Otros formatos pueden causar errores.
- **Performance**: Usa `--force` solo cuando sea necesario, ya que aumenta el tiempo de ejecución.

## Ejemplo

1. Crea un JSON en `llibrerys/vehiculos/tipo_aereo/poco/elfico/VEH001.json`:
   ```json
   {