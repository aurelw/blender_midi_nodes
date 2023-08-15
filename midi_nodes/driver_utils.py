import bpy

def update_drivers_on_animation_data(anim_data):
    """Hacky workaround to trigger driver update."""
    for driver in anim_data.drivers:
        print("Update Driver")
        driver.driver.expression += " "
        driver.driver.expression = driver.driver.expression[:-1]


def update_drivers_for_ids(ids):
    for identity in ids:
        if hasattr(identity, "animation_data") and \
           identity.animation_data:
            update_drivers_on_animation_data(identity.animation_data)

def update_all_drivers():
    update_drivers_for_ids(bpy.data.objects)
    update_drivers_for_ids(bpy.data.shape_keys)
    for node_group in bpy.data.node_groups:
        update_drivers_for_ids(node_group.nodes)

    
