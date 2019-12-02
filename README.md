# Sprite Detection

## Sprite

A [**sprite**](<https://en.wikipedia.org/wiki/Sprite_(computer_graphics)>) is a small [**raster graphic**](https://en.wikipedia.org/wiki/Raster_graphics) (a **bitmap**) that represents an object such as a character, a vehicle, a projectile, etc..

## Sprite Mask

The mask of a sprite defines the 2D shape of the sprite. For example, the sprite sheet [`metal_slug_sprite_standing_stance.png`](image/metal_slug_sprite_standing_stance_large.png) contains the 3 following sprites:

![Metal Slug Standing Stance](image/metal_slug_sprite_standing_stance_large.png)

The masks of these sprites are respectively:

![](image/metal_slug_sprite_detection_coloring.png)


Other example with the following image:

![](image/optimized_sprite_sheet.png)

```python
>>> from PIL import Image
>>> image = Image.open('optimized_sprite_sheet.png')
>>> sprites, label_map = find_sprites(image)
>>> len(sprites)
22
>>> for label, sprite in sprites.items():
...     print(f"Sprite ({label}): [{sprite.top_left}, {sprite.bottom_right}] {sprite.width}x{sprite.height}")
Sprite (25): [(383, 1), (455, 102)] 73x102
Sprite (43): [(9, 2), (97, 122)] 89x121
Sprite (26): [(110, 4), (195, 123)] 86x120
Sprite (46): [(207, 4), (291, 123)] 85x120
Sprite (16): [(305, 8), (379, 123)] 75x116
Sprite (53): [(349, 125), (431, 229)] 83x105
Sprite (61): [(285, 126), (330, 181)] 46x56
Sprite (100): [(1, 129), (101, 237)] 101x109
Sprite (106): [(106, 129), (193, 249)] 88x121
Sprite (93): [(183, 137), (278, 241)] 96x105
Sprite (95): [(268, 173), (355, 261)] 88x89
Sprite (178): [(6, 244), (101, 348)] 96x105
Sprite (185): [(145, 247), (245, 355)] 101x109
Sprite (141): [(343, 257), (417, 372)] 75x116
Sprite (169): [(102, 262), (142, 303)] 41x42
Sprite (188): [(249, 267), (344, 373)] 96x107
Sprite (192): [(412, 337), (448, 372)] 37x36
Sprite (256): [(89, 353), (184, 459)] 96x107
Sprite (234): [(11, 356), (104, 461)] 94x106
Sprite (207): [(188, 358), (281, 463)] 94x106
Sprite (229): [(384, 374), (456, 475)] 73x102
Sprite (248): [(286, 378), (368, 482)] 83x105
```

# Draw Sprite Label Bounding Boxes

```python
>>> from PIL import Image
>>> image = Image.open('optimized_sprite_sheet.png')
>>> sprites, label_map = find_sprites(image)
>>> # Draw sprite masks and bounding boxes with the default white background color.
>>> sprite_label_image = create_sprite_labels_image(sprites, label_map)
>>> sprite_label_image.save('optimized_sprite_sheet_bounding_box_white_background.png')
>>> # Draw sprite masks and bounding boxes with a transparent background color.
>>> sprite_label_image = create_sprite_labels_image(sprites, label_map, background_color=(0, 0, 0, 0))
>>> sprite_label_image.save('optimized_sprite_sheet_bounding_box_transparent_background.png')
```

| Sprite Masks with White Background                            | 
| ------------------------------------------------------------- | ------------------------------------------------------------------- |
| ![](image/optimized_sprite_sheet_bounding_box_white_background.png) | ![](image/optimized_sprite_sheet_bounding_box_transparent_background.png) |
