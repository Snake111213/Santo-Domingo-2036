"""
GENERADOR DE CIUDAD INTELIGENTE 2036
Script para Blender - Ciudad del Futuro
Autor: Actuana Academy
Versión: 1.0
"""

import bpy
import random
import math
from mathutils import Vector

# ============================================
# CONFIGURACIÓN PRINCIPAL
# ============================================

CONFIG = {
    'grid_size': 12,  # Tamaño del grid (12x12 bloques)
    'block_size': 20,  # Tamaño de cada bloque en metros
    'street_width': 4,  # Ancho de calles
    'seed': 2036,  # Semilla para reproducibilidad
}

# ============================================
# FUNCIONES DE LIMPIEZA
# ============================================

def limpiar_escena():
    """Elimina todos los objetos de la escena"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Limpiar materiales huérfanos
    for material in bpy.data.materials:
        if not material.users:
            bpy.data.materials.remove(material)

# ============================================
# MATERIALES
# ============================================

def crear_materiales():
    """Crea todos los materiales necesarios"""
    materiales = {}
    
    # Material para edificios modernos (vidrio/metal)
    mat_edificio = bpy.data.materials.new(name="Edificio_Moderno")
    mat_edificio.use_nodes = True
    nodes = mat_edificio.node_tree.nodes
    nodes.clear()
    
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_bsdf.inputs['Base Color'].default_value = (0.2, 0.3, 0.4, 1.0)
    node_bsdf.inputs['Metallic'].default_value = 0.8
    node_bsdf.inputs['Roughness'].default_value = 0.2
    
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    mat_edificio.node_tree.links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])
    materiales['edificio'] = mat_edificio
    
    # Material para calles (asfalto)
    mat_calle = bpy.data.materials.new(name="Calle")
    mat_calle.use_nodes = True
    nodes = mat_calle.node_tree.nodes
    nodes.clear()
    
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_bsdf.inputs['Base Color'].default_value = (0.15, 0.15, 0.15, 1.0)
    node_bsdf.inputs['Roughness'].default_value = 0.9
    
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    mat_calle.node_tree.links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])
    materiales['calle'] = mat_calle
    
    # Material para áreas verdes
    mat_verde = bpy.data.materials.new(name="Area_Verde")
    mat_verde.use_nodes = True
    nodes = mat_verde.node_tree.nodes
    nodes.clear()
    
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_bsdf.inputs['Base Color'].default_value = (0.1, 0.4, 0.1, 1.0)
    node_bsdf.inputs['Roughness'].default_value = 0.95
    
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    mat_verde.node_tree.links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])
    materiales['verde'] = mat_verde
    
    # Material para paneles solares
    mat_solar = bpy.data.materials.new(name="Panel_Solar")
    mat_solar.use_nodes = True
    nodes = mat_solar.node_tree.nodes
    nodes.clear()
    
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.2, 1.0)
    node_bsdf.inputs['Metallic'].default_value = 0.9
    node_bsdf.inputs['Roughness'].default_value = 0.1
    
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    mat_solar.node_tree.links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])
    materiales['solar'] = mat_solar
    
    # Material para luces LED (emisivo)
    mat_led = bpy.data.materials.new(name="LED_Luz")
    mat_led.use_nodes = True
    nodes = mat_led.node_tree.nodes
    nodes.clear()
    
    node_emission = nodes.new(type='ShaderNodeEmission')
    node_emission.inputs['Color'].default_value = (0.8, 0.9, 1.0, 1.0)
    node_emission.inputs['Strength'].default_value = 5.0
    
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    mat_led.node_tree.links.new(node_emission.outputs['Emission'], node_output.inputs['Surface'])
    materiales['led'] = mat_led
    
    return materiales

# ============================================
# GENERACIÓN DE CALLES
# ============================================

def crear_grid_calles(grid_size, block_size, street_width, materiales):
    """Crea el sistema de calles en grid"""
    total_size = grid_size * block_size
    
    # Crear calles horizontales
    for i in range(grid_size + 1):
        y_pos = i * block_size - total_size / 2
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(0, y_pos, -0.05)
        )
        calle = bpy.context.active_object
        calle.name = f"Calle_H_{i}"
        calle.scale = (total_size, street_width, 0.1)
        calle.data.materials.append(materiales['calle'])
    
    # Crear calles verticales
    for i in range(grid_size + 1):
        x_pos = i * block_size - total_size / 2
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x_pos, 0, -0.05)
        )
        calle = bpy.context.active_object
        calle.name = f"Calle_V_{i}"
        calle.scale = (street_width, total_size, 0.1)
        calle.data.materials.append(materiales['calle'])

# ============================================
# GENERACIÓN DE EDIFICIOS
# ============================================

def crear_edificio_inteligente(x, y, tipo, materiales):
    """Crea un edificio inteligente con características específicas"""
    
    # Parámetros según tipo
    if tipo == 'alto':
        altura = random.uniform(30, 60)
        ancho = random.uniform(8, 12)
        profundidad = random.uniform(8, 12)
    elif tipo == 'medio':
        altura = random.uniform(15, 30)
        ancho = random.uniform(6, 10)
        profundidad = random.uniform(6, 10)
    else:  # bajo
        altura = random.uniform(5, 15)
        ancho = random.uniform(5, 8)
        profundidad = random.uniform(5, 8)
    
    # Crear edificio base
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x, y, altura/2)
    )
    edificio = bpy.context.active_object
    edificio.name = f"Edificio_{tipo}_{x}_{y}"
    edificio.scale = (ancho, profundidad, altura)
    edificio.data.materials.append(materiales['edificio'])
    
    # Agregar paneles solares en el techo
    if random.random() > 0.3:  # 70% de edificios tienen paneles
        panel_offset = altura/2 + 0.2
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x, y, panel_offset)
        )
        panel = bpy.context.active_object
        panel.name = f"Panel_Solar_{x}_{y}"
        panel.scale = (ancho * 0.9, profundidad * 0.9, 0.3)
        panel.data.materials.append(materiales['solar'])
    
    # Agregar antenas/sensores IoT
    if tipo in ['alto', 'medio'] and random.random() > 0.5:
        antena_offset = altura/2 + 1
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.2,
            depth=2,
            location=(x, y, antena_offset)
        )
        antena = bpy.context.active_object
        antena.name = f"Antena_IoT_{x}_{y}"
        
        # Agregar luz LED en la antena
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.3,
            location=(x, y, antena_offset + 1.2)
        )
        luz_antena = bpy.context.active_object
        luz_antena.name = f"LED_Antena_{x}_{y}"
        luz_antena.data.materials.append(materiales['led'])

# ============================================
# ILUMINACIÓN INTELIGENTE
# ============================================

def crear_poste_luz_inteligente(x, y, materiales):
    """Crea un poste de luz LED inteligente"""
    
    # Poste
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.15,
        depth=6,
        location=(x, y, 3)
    )
    poste = bpy.context.active_object
    poste.name = f"Poste_Luz_{x}_{y}"
    
    # Luminaria LED
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x, y, 6.5)
    )
    luminaria = bpy.context.active_object
    luminaria.name = f"Luminaria_LED_{x}_{y}"
    luminaria.scale = (0.8, 0.8, 0.3)
    luminaria.data.materials.append(materiales['led'])
    
    # Agregar luz real
    bpy.ops.object.light_add(
        type='POINT',
        location=(x, y, 6.5)
    )
    luz = bpy.context.active_object
    luz.name = f"Luz_LED_{x}_{y}"
    luz.data.energy = 100
    luz.data.color = (0.8, 0.9, 1.0)

# ============================================
# ÁREAS VERDES Y PARQUES
# ============================================

def crear_parque_urbano(x, y, size, materiales):
    """Crea un área verde/parque urbano"""
    
    # Base del parque
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x, y, 0.05)
    )
    parque = bpy.context.active_object
    parque.name = f"Parque_{x}_{y}"
    parque.scale = (size, size, 0.1)
    parque.data.materials.append(materiales['verde'])
    
    # Agregar algunos "árboles" simples
    num_arboles = random.randint(3, 8)
    for _ in range(num_arboles):
        offset_x = random.uniform(-size/3, size/3)
        offset_y = random.uniform(-size/3, size/3)
        
        # Tronco
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.3,
            depth=4,
            location=(x + offset_x, y + offset_y, 2)
        )
        
        # Copa
        bpy.ops.mesh.primitive_ico_sphere_add(
            radius=2,
            location=(x + offset_x, y + offset_y, 5)
        )
        copa = bpy.context.active_object
        copa.data.materials.append(materiales['verde'])

# ============================================
# INFRAESTRUCTURA INTELIGENTE
# ============================================

def crear_estacion_carga(x, y, materiales):
    """Crea una estación de carga para vehículos eléctricos"""
    
    # Base
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x, y, 1.5)
    )
    estacion = bpy.context.active_object
    estacion.name = f"Estacion_Carga_{x}_{y}"
    estacion.scale = (1.5, 0.5, 3)
    
    # Panel con LED
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x, y + 0.3, 2)
    )
    panel = bpy.context.active_object
    panel.scale = (1.2, 0.1, 1.5)
    panel.data.materials.append(materiales['led'])

# ============================================
# GENERADOR PRINCIPAL
# ============================================

def generar_ciudad_inteligente():
    """Función principal que genera toda la ciudad"""
    
    print("=" * 50)
    print("GENERANDO CIUDAD INTELIGENTE 2036")
    print("=" * 50)
    
    # Configurar semilla para reproducibilidad
    random.seed(CONFIG['seed'])
    
    # Limpiar escena
    print("Limpiando escena...")
    limpiar_escena()
    
    # Crear materiales
    print("Creando materiales...")
    materiales = crear_materiales()
    
    # Crear grid de calles
    print("Generando red de calles...")
    crear_grid_calles(
        CONFIG['grid_size'],
        CONFIG['block_size'],
        CONFIG['street_width'],
        materiales
    )
    
    # Generar edificios en cada bloque
    print("Generando edificios inteligentes...")
    block_size = CONFIG['block_size']
    grid_size = CONFIG['grid_size']
    total_size = grid_size * block_size
    
    edificios_creados = 0
    parques_creados = 0
    
    for i in range(grid_size):
        for j in range(grid_size):
            # Calcular posición central del bloque
            x = i * block_size - total_size/2 + block_size/2
            y = j * block_size - total_size/2 + block_size/2
            
            # Decidir qué poner en este bloque
            rand = random.random()
            
            if rand < 0.15:  # 15% parques
                crear_parque_urbano(x, y, block_size * 0.8, materiales)
                parques_creados += 1
            else:  # Edificios
                # Determinar tipo de edificio
                tipo_rand = random.random()
                if tipo_rand < 0.2:
                    tipo = 'alto'
                elif tipo_rand < 0.6:
                    tipo = 'medio'
                else:
                    tipo = 'bajo'
                
                crear_edificio_inteligente(x, y, tipo, materiales)
                edificios_creados += 1
    
    # Agregar iluminación inteligente en intersecciones
    print("Instalando iluminación LED inteligente...")
    luces_creadas = 0
    
    for i in range(grid_size + 1):
        for j in range(grid_size + 1):
            x = i * block_size - total_size/2
            y = j * block_size - total_size/2
            
            crear_poste_luz_inteligente(x, y, materiales)
            luces_creadas += 1
    
    # Agregar estaciones de carga
    print("Instalando estaciones de carga eléctrica...")
    estaciones_creadas = 0
    
    for i in range(0, grid_size, 3):
        for j in range(0, grid_size, 3):
            x = i * block_size - total_size/2 + block_size/4
            y = j * block_size - total_size/2 + block_size/4
            
            crear_estacion_carga(x, y, materiales)
            estaciones_creadas += 1
    
    # Configurar cámara
    print("Configurando cámara...")
    bpy.ops.object.camera_add(location=(total_size * 0.8, total_size * 0.8, total_size * 0.6))
    camara = bpy.context.active_object
    camara.rotation_euler = (math.radians(60), 0, math.radians(45))
    bpy.context.scene.camera = camara
    
    # Configurar iluminación ambiental
    print("Configurando iluminación ambiental...")
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 100))
    sol = bpy.context.active_object
    sol.data.energy = 2
    sol.rotation_euler = (math.radians(45), 0, math.radians(30))
    
    # Configurar mundo (cielo)
    world = bpy.context.scene.world
    world.use_nodes = True
    world_nodes = world.node_tree.nodes
    world_nodes.clear()
    
    node_background = world_nodes.new(type='ShaderNodeBackground')
    node_background.inputs['Color'].default_value = (0.3, 0.5, 0.8, 1.0)
    node_background.inputs['Strength'].default_value = 0.8
    
    node_output = world_nodes.new(type='ShaderNodeOutputWorld')
    world.node_tree.links.new(node_background.outputs['Background'], node_output.inputs['Surface'])
    
    # Resumen
    print("\n" + "=" * 50)
    print("CIUDAD INTELIGENTE 2036 - COMPLETADA")
    print("=" * 50)
    print(f"Edificios creados: {edificios_creados}")
    print(f"Parques urbanos: {parques_creados}")
    print(f"Postes de luz LED: {luces_creadas}")
    print(f"Estaciones de carga: {estaciones_creadas}")
    print(f"Área total: {total_size}m x {total_size}m")
    print("=" * 50)
    print("\nConsejos:")
    print("- Presiona '0' en el numpad para ver desde la cámara")
    print("- Presiona 'Z' y selecciona 'Rendered' para ver la ciudad completa")
    print("- Usa el modificador 'Array' en edificios para crear más variaciones")
    print("- Puedes cambiar CONFIG al inicio del script para ajustar parámetros")

# ============================================
# EJECUTAR
# ============================================

if __name__ == "__main__":
    generar_ciudad_inteligente()