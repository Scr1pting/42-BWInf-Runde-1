# Arukone

**Team-ID:** ==XYZ== <br>
**Autor:** Jonas B <br>
**Datum:** 26. Oktober 2023

## Inhaltsverzeichnis

1. [Lösungsidee](#lösungsidee)
2. [Umsetzung](#umsetzung)
3. [Beispiele](#beispiele)

## Lösungsidee

Das Programm erstellt zufällig aufgebaute Arukino-Puzzel. Danach überprüft es, ob das Arukino lösbar ist. Der Prozess wird so lange wiederholt, bis ein lösbares Arukino-Puzzel entsteht und es ausgegeben wird.

## Umsetzung

Die Lösungsidee wird in Python implementiert.

```mermaid
flowchart TB
    Nutzer -- Konstruktionspfad, <br> Speicherungseinstellung --> start_command_line_interface
    start_command_line_interface -- Konstruktion --> generate_table
    start_command_line_interface -- Tabelle --> Nutzer
    generate_table -- Tabelle --> start_command_line_interface
    generate_table -- Konstruktion --> generate_lights_matrix 
    generate_lights_matrix -- Licht Matrix --> generate_table
```

## Beispiele



## Quelltext

