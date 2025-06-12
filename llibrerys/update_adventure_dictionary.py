import os
import json
import argparse
import time
import logging
from pathlib import Path

def setup_logging(log_file=None):
    """Configura el logging a consola y, opcionalmente, a un archivo."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logging.getLogger().addHandler(file_handler)

def validate_entry(entry, file_path, is_subentity=False):
    """Valida que una entidad tenga los campos requeridos."""
    required_fields = ["id", "name"]
    if not is_subentity:  # Las entidades principales también necesitan 'type'
        required_fields.append("type")
    for field in required_fields:
        if field not in entry or not entry[field]:
            logging.warning(f"Entidad inválida en {file_path}: falta el campo '{field}'")
            return False
    return True

def update_adventure_dictionary(root_path="llibrerys", output_file="llibrerys/adventu_dic.json", force=False, exclude_dirs=None, log_file=None):
    """
    Recorre las carpetas en llibrerys/, recopila JSONs de cualquier tipo de entidad,
    maneja múltiples entidades por JSON, elimina entidades obsoletas, y actualiza
    adventu_dic.json con un diccionario dinámico de elementos. Optimizado para carpetas grandes.
    
    Args:
        root_path (str): Carpeta raíz.
        output_file (str): Archivo de salida.
        force (bool): Procesa todos los JSONs si True.
        exclude_dirs (list): Carpetas a excluir.
        log_file (str): Archivo de log opcional.
    """
    start_time = time.time()
    setup_logging(log_file)
    
    # Inicializar el diccionario nuevo
    new_dictionary = {
        "items": [],
        "monstruos": [],
        "conjuros": [],
        "pnjs": [],
        "localizaciones": []
    }
    
    # Cargar el diccionario existente para indexar paths
    existing_paths = set()
    if Path(output_file).exists():
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_dict = json.load(f)
                existing_paths = {entry["path"] for entries in existing_dict.values() for entry in entries}
            logging.info(f"Cargado diccionario existente con {len(existing_paths)} paths")
        except json.JSONDecodeError:
            logging.error(f"{output_file} malformado, iniciando diccionario nuevo")
        except Exception as e:
            logging.error(f"Error al cargar {output_file}: {e}")
    
    # Procesar JSONs y recopilar entidades
    seen_ids = {}  # Mapear (category, id) a file_path para detectar colisiones
    exclude_dirs = set(exclude_dirs or [])
    
    def add_entry(category, entry, file_path):
        """Añade una entrada al diccionario, detectando colisiones."""
        entry_id = entry.get("id")
        if not entry_id:
            return
        key = (category, entry_id)
        if key in seen_ids:
            logging.warning(f"Colisión de ID: {entry_id} en {category}. Existente: {seen_ids[key]}, Nueva: {file_path}")
            return  # Mantener la primera entrada
        if validate_entry(entry, file_path, is_subentity=(category != entry.get("type") + "s")):
            entry["path"] = str(Path(file_path).resolve())
            new_dictionary[category].append(entry)
            seen_ids[key] = file_path
    
    # Recorrer recursivamente llibrerys/
    processed_files = 0
    for root, dirs, files in os.walk(root_path):
        # Excluir carpetas
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                # Saltar si no es --force y el path ya existe
                if not force and file_path in existing_paths:
                    continue
                processed_files += 1
                try:
                    # Intentar múltiples codificaciones
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                    except UnicodeDecodeError:
                        with open(file_path, 'r', encoding='latin-1') as f:
                            data = json.load(f)
                            logging.warning(f"{file_path} usa codificación latin-1")
                    
                    # Procesar entidad principal
                    item_type = data.get("type", "").lower()
                    if item_type:
                        entry = {
                            "id": data.get("id", ""),
                            "name": data.get("name", ""),
                            "type": item_type,
                            "description": data.get("description", ""),
                            "origen": data.get("origen", "")
                        }
                        
                        if item_type == "item":
                            entry.update({
                                "rareza": data.get("rareza", ""),
                                "subtype": data.get("subtype", "")
                            })
                            add_entry("items", entry, file_path)
                        
                        elif item_type == "monster":
                            entry.update({
                                "cr": data.get("cr", 0),
                                "tamaño": data.get("tamaño", ""),
                                "alineamiento": data.get("alineamiento", "")
                            })
                            add_entry("monstruos", entry, file_path)
                        
                        elif item_type == "spell":
                            entry.update({
                                "nivel": data.get("nivel", 0),
                                "escuela": data.get("escuela", ""),
                                "clase": data.get("clase", [])
                            })
                            add_entry("conjuros", entry, file_path)
                        
                        elif item_type == "pnj":
                            entry.update({
                                "role": data.get("role", "")
                            })
                            add_entry("pnjs", entry, file_path)
                        
                        elif item_type == "location":
                            add_entry("localizaciones", entry, file_path)
                        
                        elif item_type == "adventure":
                            for pnj in data.get("pnjs", []):
                                pnj_entry = {
                                    "id": pnj.get("id", ""),
                                    "name": pnj.get("name", ""),
                                    "type": "pnj",
                                    "description": pnj.get("description", ""),
                                    "origen": data.get("origen", ""),
                                    "role": pnj.get("role", "")
                                }
                                add_entry("pnjs", pnj_entry, file_path)
                            
                            for loc in data.get("localizaciones", []):
                                loc_entry = {
                                    "id": loc.get("id", ""),
                                    "name": loc.get("name", ""),
                                    "type": "location",
                                    "description": loc.get("description", ""),
                                    "origen": data.get("origen", "")
                                }
                                add_entry("localizaciones", loc_entry, file_path)
                            
                            for item in data.get("items", []):
                                item_entry = {
                                    "id": item.get("id", ""),
                                    "name": item.get("name", ""),
                                    "type": "item",
                                    "description": item.get("description", ""),
                                    "origen": data.get("origen", ""),
                                    "rareza": item.get("rareza", ""),
                                    "subtype": item.get("subtype", "")
                                }
                                add_entry("items", item_entry, file_path)
                            
                            for monster in data.get("monstruos", []):
                                monster_entry = {
                                    "id": monster.get("id", ""),
                                    "name": monster.get("name", ""),
                                    "type": "monster",
                                    "description": monster.get("description", ""),
                                    "origen": data.get("origen", ""),
                                    "cr": monster.get("cr", 0),
                                    "tamaño": monster.get("tamaño", ""),
                                    "alineamiento": monster.get("alineamiento", "")
                                }
                                add_entry("monstruos", monster_entry, file_path)
                            
                            for spell in data.get("conjuros", []):
                                spell_entry = {
                                    "id": spell.get("id", ""),
                                    "name": spell.get("name", ""),
                                    "type": "spell",
                                    "description": spell.get("description", ""),
                                    "origen": data.get("origen", ""),
                                    "nivel": spell.get("nivel", 0),
                                    "escuela": spell.get("escuela", ""),
                                    "clase": spell.get("clase", [])
                                }
                                add_entry("conjuros", spell_entry, file_path)
                        
                        else:
                            # Nuevo tipo de entidad
                            plural_type = item_type + "s" if not item_type.endswith("s") else item_type
                            if plural_type not in new_dictionary:
                                new_dictionary[plural_type] = []
                            add_entry(plural_type, entry, file_path)
                    
                    # Procesar listas de entidades
                    for key in ["items", "monstruos", "conjuros", "pnjs", "localizaciones"]:
                        if key in data and isinstance(data[key], list):
                            category = key
                            for sub_entity in data[key]:
                                sub_entry = {
                                    "id": sub_entity.get("id", ""),
                                    "name": sub_entity.get("name", ""),
                                    "type": key[:-1] if key != "localizaciones" else "location",
                                    "description": sub_entity.get("description", ""),
                                    "origen": sub_entity.get("origen", data.get("origen", ""))
                                }
                                if key == "items":
                                    sub_entry.update({
                                        "rareza": sub_entity.get("rareza", ""),
                                        "subtype": sub_entity.get("subtype", "")
                                    })
                                elif key == "monstruos":
                                    sub_entry.update({
                                        "cr": sub_entity.get("cr", 0),
                                        "tamaño": sub_entity.get("tamaño", ""),
                                        "alineamiento": sub_entity.get("alineamiento", "")
                                    })
                                elif key == "conjuros":
                                    sub_entry.update({
                                        "nivel": sub_entity.get("nivel", 0),
                                        "escuela": sub_entity.get("escuela", ""),
                                        "clase": sub_entity.get("clase", [])
                                    })
                                elif key == "pnjs":
                                    sub_entry.update({
                                        "role": sub_entity.get("role", "")
                                    })
                                add_entry(category, sub_entry, file_path)
                    
                except json.JSONDecodeError:
                    logging.error(f"JSON malformado en {file_path}")
                except Exception as e:
                    logging.error(f"Error al procesar {file_path}: {e}")
    
    # Guardar el diccionario actualizado
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(new_dictionary, f, indent=2, ensure_ascii=False)
        end_time = time.time()
        logging.info(f"Diccionario actualizado en {output_file}")
        logging.info(f"Entidades procesadas: {sum(len(entries) for entries in new_dictionary.values())}")
        logging.info(f"Archivos procesados: {processed_files}")
        logging.info(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
        logging.info(f"Modo force: {'activado' if force else 'desactivado'}")
    except Exception as e:
        logging.error(f"Error al guardar {output_file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Actualiza el diccionario de entidades para D&D 5e 2024.")
    parser.add_argument("root_path", nargs="?", default="llibrerys", help="Carpeta raíz (default: llibrerys)")
    parser.add_argument("output_file", nargs="?", default="llibrerys/adventu_dic.json", help="Archivo de salida (default: llibrerys/adventu_dic.json)")
    parser.add_argument("-f", "--force", action="store_true", help="Procesa todos los JSONs, incluso si no han cambiado")
    parser.add_argument("--exclude", nargs="*", default=[], help="Carpetas a excluir (ej. backups temp)")
    parser.add_argument("--log", help="Archivo de log para registrar acciones")
    args = parser.parse_args()
    
    update_adventure_dictionary(args.root_path, args.output_file, args.force, args.exclude, args.log)