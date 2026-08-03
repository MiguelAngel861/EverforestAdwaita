# Instrucciones de Memoria y Contexto para Agentes de IA

Este documento establece las reglas obligatorias de interacción para cualquier agente de IA que trabaje en este repositorio. Su objetivo es garantizar la continuidad del desarrollo entre diferentes sesiones y ejecuciones.

---

## 📌 La Regla de Oro (Golden Rule)

El proyecto cuenta con un archivo de registro histórico y persistente localizado en [docs/memory.json](file:///home/damian/Projects/EverforestAdwaita/docs/memory.json). Todo agente **DEBE** cumplir estrictamente con el siguiente protocolo:

### 1. Al Iniciar una Nueva Sesión (Lectura)
Antes de realizar cualquier propuesta, cambio o análisis:
- **Lee las últimas entradas de [docs/memory.json](file:///home/damian/Projects/EverforestAdwaita/docs/memory.json)**.
- Entiende el contexto actual, qué se hizo en la sesión anterior, qué decisiones de diseño se tomaron y cuáles son los objetivos inmediatos.
- Si necesitas ubicar cuándo ocurrió algún cambio o por qué se tomó una decisión específica, consulta el historial de este archivo.

### 2. Durante la Sesión (Desarrollo)
- Sigue las decisiones de diseño previas (ej. mantener el sistema de esquinas de 90 grados, no introducir dependencias pesadas innecesarias como Meson si no es indispensable, mantener compatibilidad dual GTK 3 / GTK 4, etc.).

### 3. Al Finalizar una Sesión (Escritura)
Antes de despedirte o dar por concluido tu turno:
- **Actualiza [docs/memory.json](file:///home/damian/Projects/EverforestAdwaita/docs/memory.json)** agregando un nuevo objeto JSON al arreglo con los detalles de tu sesión.
- Utiliza la estructura obligatoria definida en la plantilla **[docs/templates/memory_template.json](file:///home/damian/Projects/EverforestAdwaita/docs/templates/memory_template.json)**.

---

## 📂 Archivos de Referencia de Contexto

- **[docs/memory.json](file:///home/damian/Projects/EverforestAdwaita/docs/memory.json)**: Archivo JSON con la lista de sesiones históricas.
- **[docs/templates/memory_template.json](file:///home/damian/Projects/EverforestAdwaita/docs/templates/memory_template.json)**: Plantilla del formato de entrada para la memoria de los agentes.
- **[README.md](file:///home/damian/Projects/EverforestAdwaita/README.md)**: Manual de uso general del tema (cómo compilar, probar, refrescar e instalar).
