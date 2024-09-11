# MouseReactiveRGB

[![Github All Releases](https://img.shields.io/github/downloads/odizinne/MouseReactiveRGB/total.svg)]()
[![license](https://img.shields.io/github/license/odizinne/MouseReactiveRGB)]()

Reactive effect on mouse button press.
This is a personal project, far from perfect but enough for my use.

Windows / Linux (x11 works, wayland untested)

![image](assets/screenshot.png)

## Requirements

- OpenRGB Server running (OpenRGB 0.9 only. 0.91 not working yet)

Download it manually from [openrgb.org](https://openrgb.org/releases.html) or install it with my [OpenRGB-Installer](https://github.com/Odizinne/OpenRGB-Installer/releases/latest) (Windows only)
- Direct mode compatible mouse

It will use the first detected mouse with direct mode support.

Mouse requirement is an arbitrary limitation, i just find it more logic to have mouse click reactive effect showing on a mouse rather than on a fan.  
It could work with any direct mode compatible device, feel free to edit the code to allow it.

Do not ever try to remove direct mode support limitation or you'll burn your controller flash.

## Download

Download latest [release](https://github.com/Odizinne/MouseReactiveRGB/releases/latest) and run `MouseReactiveRGB.exe`.  
It will auto connect to OpenRGB server if found or will wait for it to be available.

## Settings

Settings are auto saved on window closed.

- `OpenRGB SDK IP / Port`  
Do not touch if unsure / using OpenRGB on the same PC

- `Autostart effect`  
Reactive effect will start alongside the application

- `Trigger effect on` "Left click" "Left / Right" "Any buttons"  
Select which button press should be monitored to trigger the effect.  
Should work with Left (MB1), Right (MB2), Middle (MB3), Back (MB4), Forward (MB5).

- `Color mode` "Custom" "Random" "Accent"  
Custom use values from Colors.  
Random generate a new color on every button press.  
Accent will use system accent color (Windows only).

- `Colors`
If you are unfamiliar with RGB or HEX color values, get help from a [color picker](https://www.google.com/search?q=color+picker&sca_upv=1).

- `Brightness` "0 - 100"  
Color brightness.

- `Saturation` "0 - 100"  
Color saturation.

- `Fade duration` "250ms - 2000ms"  
Duration for the fade effect.

- `FPS` "10 - 60"  
More FPS = Smoother.  
Try to lower FPS if device is acting strange.

- `Fade on release`
Fade effect will start only on button release.  
Color will be held as long as mouse button is pressed.

## Credits

- [jath03](https://github.com/jath03/openrgb-python) for openrgb-python

## Wrong mouse is being detected

"Why do you even use two mice?"
