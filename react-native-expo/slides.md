---
theme: bricks
title: Programación III - React Native con Expo
download: true
info: |
  React Native con Expo - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: react native, expo, mobile, ios, android, expo router, INSPT, UTN
transition: slide-left
mdc: true
---

# React Native con Expo

Programación III

<div class="flex gap-8 justify-end mr-16 mt-6 items-center">
<img src="/logos/react.svg" alt="React Native" class="h-12 opacity-90" />
<img src="/logos/expo.svg" alt="Expo" class="h-12 opacity-90" />
</div>

<div class="abs-b mb-8 text-sm opacity-60">
INSPT - UTN · Ciclo Lectivo 2026
</div>

---
layout: default
---

# ¿Qué es React Native?

- Un framework para escribir apps **nativas** de iOS y Android con el mismo modelo de componentes, estado y props — un solo código fuente, dos plataformas.
- No es una página web metida en un WebView: `<View>`, `<Text>`, `<Pressable>` se traducen a componentes nativos reales de cada sistema operativo, no a `<div>`/`<span>` de HTML.
- El JavaScript corre en su propio motor (Hermes) y se comunica con el lado nativo — la UI que se ve en pantalla es nativa de verdad, no renderizada dentro de un navegador embebido.

<div class="flex gap-10 justify-center mt-6 items-center">
<img src="/logos/react.svg" alt="React Native" class="h-12 opacity-80" />
</div>

---
layout: default
---

# ¿Qué es Expo?

- Una capa sobre React Native que resuelve todo lo que React Native por sí solo deja a mano: configurar Xcode/Android Studio, compilar binarios, acceder a cámara/ubicación/notificaciones sin escribir código nativo.
- Un conjunto de paquetes (`expo-*`) con APIs nativas ya listas para usar desde JavaScript/TypeScript, con versiones mantenidas en conjunto para que no choquen entre sí.
- Compilación de binarios **en la nube** (EAS Build) — no hace falta tener Xcode instalado para generar una build de iOS.

<div class="mt-3 text-sm italic opacity-80 text-center">

No es un fork de React Native ni lo reemplaza — es la forma recomendada hoy de empezar un proyecto nuevo, incluso por el propio equipo de React Native.

</div>

---
layout: default
---

# Historia breve

- **2015** — Facebook libera **React Native**: "aprendé una vez, escribí en cualquier lado", mismo modelo mental que React, apps nativas de verdad.
- **2018** — Expo introduce el *managed workflow*: empezar sin configurar nada nativo a mano.
- **2023** — la **New Architecture** (motor Hermes + Fabric + TurboModules) llega como opción, con mejor rendimiento y comunicación nativo↔JS.
- **2026** — la New Architecture pasa a ser la **única** (la Legacy se discontinúa), y **Expo Router** reemplaza la navegación configurada a mano como forma por defecto de rutear.
- **Hoy** — Expo SDK 58, sobre React Native 0.88 y React 19.

---
layout: center
---

# Empezar un proyecto

---
layout: default
---

# Crear un proyecto

```bash
npx create-expo-app@latest mi-app
cd mi-app
npx expo start
```

<div class="mt-3 text-sm opacity-80">

Arma un proyecto con TypeScript y ruteo por archivos (Expo Router) ya configurados. `expo start` levanta un servidor de desarrollo y muestra un código QR — sin ejecutar nada nativo todavía.

</div>

<div class="mt-1 text-xs opacity-60">

→ [docs.expo.dev/get-started/create-a-project](https://docs.expo.dev/get-started/create-a-project/)

</div>

---
layout: default
---

# Ejecutar la app

<div class="grid grid-cols-2 gap-4 mt-2">
<div class="p-3 rounded-lg border border-blue-300 bg-blue-50">
<strong>Expo Go</strong><br/>
Una app descargable de las stores — escanea el QR de <code>expo start</code> y corre el proyecto adentro, al instante. Sin compilar nada. Ideal para empezar.
</div>
<div class="p-3 rounded-lg border border-purple-300 bg-purple-50">
<strong>Simulador/emulador</strong><br/>
iOS Simulator (necesita macOS + Xcode) o un emulador de Android (Android Studio) — corriendo en la propia computadora, sin un teléfono físico.
</div>
</div>

<div class="mt-4 text-sm opacity-80">

Los tres caminos corren el **mismo código** — cambiar de uno a otro no requiere tocar el proyecto.

</div>

---
layout: default
---

# Estructura del proyecto

```
mi-app/
├── app/
│   ├── _layout.tsx      # layout raíz
│   └── index.tsx        # pantalla "/"
├── assets/               # imágenes, fuentes
├── app.json              # nombre, ícono, splash screen
└── package.json
```

<div class="mt-2 text-sm opacity-80">

`app/` es exactamente la misma idea que un sitio con ruteo por archivos en la web — cada archivo es una pantalla. `app.json` reemplaza al `AndroidManifest.xml`/`Info.plist` que normalmente habría que editar a mano en cada plataforma.

</div>

---
layout: center
---

# Componentes nativos básicos

---
layout: default
---

# No hay HTML

```tsx
import { View, Text } from 'react-native'

export default function HomeScreen() {
  return (
    <View>
      <Text>Hola desde el celular</Text>
    </View>
  )
}
```

<div class="mt-3 text-sm opacity-80">

`<View>` reemplaza a `<div>`, `<Text>` a cualquier texto — y es **obligatorio**: un string suelto (sin `<Text>` alrededor) directamente no renderiza. No hay `<p>`, `<span>`, `<button>` — un número chico de componentes base, que mapean 1 a 1 a algo nativo.

</div>

---
layout: default
---

# Estilos con `StyleSheet`

```tsx
import { View, Text, StyleSheet } from 'react-native'

export default function Card() {
  return (
    <View style={styles.card}>
      <Text style={styles.title}>Producto</Text>
    </View>
  )
}

const styles = StyleSheet.create({
  card: { padding: 16, borderRadius: 8, backgroundColor: 'white' },
  title: { fontSize: 18, fontWeight: 'bold' },
})
```

<div class="mt-1 text-xs opacity-80">

Sin CSS: los estilos son objetos JS, con las mismas propiedades (`padding`, `backgroundColor`) pero en *camelCase* y sin unidades (los números son *density-independent pixels*). Todo contenedor es `flex` por defecto, con `flexDirection: 'column'` (al revés que en la web).

</div>

---
layout: default
---

# Interactividad

<div class="grid grid-cols-2 gap-3 text-sm">
<div>

```tsx
import { useState } from 'react'
import { View, Text, Pressable } from 'react-native'

export default function Counter() {
  const [count, setCount] = useState(0)
  return (
    <View style={styles.container}>
      <Text>Contador: {count}</Text>
      <Pressable
        style={styles.button}
        onPress={() => setCount((c) => c + 1)}
      >
        <Text style={styles.buttonText}>Sumar</Text>
      </Pressable>
    </View>
  )
}
```

</div>
<div>

```tsx
const styles = StyleSheet.create({
  container: { alignItems: 'center', gap: 12 },
  button: {
    backgroundColor: '#4f46e5',
    padding: 10,
    borderRadius: 8,
  },
  buttonText: { color: 'white' },
})
```

<div class="mt-2 text-xs opacity-80">

Mismo `useState` de siempre. `<Pressable>` reemplaza a un `<button onClick>` — los eventos táctiles tienen sus propios nombres (`onPress`, `onLongPress`).

</div>

</div>
</div>

---
layout: default
---

# Listas: `FlatList`

```tsx
import { FlatList, Text } from 'react-native'

const products = [{ id: '1', name: 'Mouse' }, { id: '2', name: 'Teclado' }]

export default function ProductList() {
  return (
    <FlatList
      data={products}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <Text>{item.name}</Text>}
    />
  )
}
```

<div class="mt-2 text-sm opacity-80">

Un `.map()` común renderiza **todos** los elementos de una, aunque la mayoría no esté visible en pantalla. `<FlatList>` solo renderiza lo que entra en el viewport (más un margen) y recicla las celdas al hacer scroll — indispensable con listas largas en un dispositivo con memoria limitada.

</div>

---
layout: center
---

# Ruteo con Expo Router

---
layout: default
---

# Ruteo por archivos

```
app/
├── _layout.tsx       # layout raíz
├── index.tsx         # pantalla "/"
└── profile.tsx       # pantalla "/profile"
```

<div class="mt-3 text-sm opacity-80">

Misma filosofía que un framework web con ruteo por archivos: cada archivo en `app/` es una pantalla navegable, sin configurar manualmente un árbol de rutas. `_layout.tsx` envuelve las pantallas de su carpeta, igual que un layout compartido.

</div>

<div class="mt-1 text-xs opacity-60">

→ [docs.expo.dev/router/introduction](https://docs.expo.dev/router/introduction/)

</div>

---
layout: default
---

# Layouts: `Stack`

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router'

export default function RootLayout() {
  return <Stack />
}
```

<div class="mt-3 text-sm opacity-80">

`<Stack>` es el patrón de navegación más común en mobile: cada pantalla nueva se **apila** arriba de la anterior (con una transición de deslizar), y un botón "atrás" nativo vuelve a la de abajo — el equivalente a navegar hacia adelante y atrás en un sitio web, pero con la animación propia de cada sistema operativo.

</div>

---
layout: default
---

# Tabs

```tsx
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router'

export default function TabsLayout() {
  return (
    <Tabs>
      <Tabs.Screen name="index" options={{ title: 'Inicio' }} />
      <Tabs.Screen name="profile" options={{ title: 'Perfil' }} />
    </Tabs>
  )
}
```

<div class="mt-2 text-sm opacity-80">

Los paréntesis en `(tabs)` marcan un **grupo de rutas** — organiza archivos sin agregar `/tabs` a la URL real. Adentro, cada archivo es una pestaña de la barra inferior.

</div>

---
layout: default
---

# Rutas dinámicas y navegación

<div class="grid grid-cols-2 gap-3 text-sm">
<div>

```tsx
// app/product/[id].tsx
import { View, Text } from 'react-native'
import { useLocalSearchParams, useRouter } from 'expo-router'

export default function ProductScreen() {
  const { id } = useLocalSearchParams<{ id: string }>()
  const router = useRouter()
  return (
    <View>
      <Text>Producto {id}</Text>
      <Text onPress={() => router.back()}>Volver</Text>
    </View>
  )
}
```

</div>
<div>

```tsx
import { Link } from 'expo-router'

<Link href="/product/1">
  Ver producto 1
</Link>
```

<div class="mt-2 text-xs opacity-80">

`[id]` funciona igual que en ruteo por archivos web. `<Link>` navega declarativamente; `useRouter()` da acceso imperativo.

</div>

</div>
</div>

---
layout: center
---

# APIs nativas

---
layout: default
---

# `npx expo install`, no `npm install`

```bash
npx expo install expo-image expo-location
```

<div class="mt-3 text-sm opacity-80">

Para paquetes del ecosistema Expo, `expo install` reemplaza a `npm install`: resuelve la versión **compatible** con el SDK del proyecto (no siempre la última de npm) — evita el problema típico de mobile de instalar una versión que compila pero rompe en tiempo de ejecución en un dispositivo real.

</div>

<div class="mt-1 text-xs opacity-60">

→ [docs.expo.dev/workflow/expo-cli#install](https://docs.expo.dev/workflow/expo-cli/#install)

</div>

---
layout: default
---

# Un ejemplo: `expo-image`

```tsx
import { Image } from 'expo-image'

export default function Avatar() {
  return (
    <Image
      source="https://ejemplo.com/foto.jpg"
      style={{ width: 200, height: 200 }}
      contentFit="cover"
    />
  )
}
```

<div class="mt-2 text-xs opacity-80">

Mismo patrón para cualquier API nativa: un paquete `expo-*` con API en TypeScript — acá, caché de disco/memoria y formatos modernos, sin nada nativo que configurar.

</div>

---
layout: center
---

# Ver la app en un dispositivo

---
layout: default
---

# Expo Go vs. development build

<div class="grid grid-cols-2 gap-4 mt-3">
<div class="p-3 rounded-lg border border-green-300 bg-green-50">
<strong>Expo Go</strong><br/>
Corre cualquier proyecto que solo use JavaScript + los paquetes <code>expo-*</code> estándar — sin compilar nada. Perfecto para aprender y para la mayoría de los proyectos chicos.
</div>
<div class="p-3 rounded-lg border border-orange-300 bg-orange-50">
<strong>Development build</strong><br/>
Necesaria apenas el proyecto agrega una librería nativa que Expo Go no trae preinstalada — una build propia, instalable en el teléfono, que sí la incluye.
</div>
</div>

<div class="mt-4 text-sm opacity-80">

La app final que se publica en las stores **nunca** es Expo Go — siempre es una build propia, generada con EAS Build.

</div>

---
layout: center
---

# Construir y publicar

---
layout: default
---

# EAS Build

```bash
npm install -g eas-cli
eas build --platform ios
eas build --platform android
```

<div class="mt-3 text-sm opacity-80">

Compila el binario (`.ipa`/`.apk`) **en servidores de Expo**, en la nube — no hace falta tener Xcode instalado para generar una build de iOS, ni Android Studio para una de Android. El resultado es un archivo descargable, listo para subir a la App Store/Play Store o instalar directo en un dispositivo de prueba.

</div>

<div class="mt-1 text-xs opacity-60">

→ [docs.expo.dev/build/introduction](https://docs.expo.dev/build/introduction/)

</div>

---
layout: default
---

# OTA updates

```bash
eas update --branch production --message "Fix en el checkout"
```

<div class="mt-3 text-sm opacity-80">

Un cambio que es solo JavaScript (no código nativo nuevo) se puede publicar **sin pasar por la revisión de las stores** — `expo-updates` lo descarga la próxima vez que la app arranca. Tiene un límite real: un ícono nuevo, una librería nativa agregada, o un cambio de permisos sí necesitan una build y revisión nuevas.

</div>

---
layout: center
---

# Cierre

---
layout: default
---

# ¿Cuándo conviene React Native con Expo?

<div class="grid grid-cols-2 gap-6 mt-2">
<div class="p-4 rounded-lg border-2 border-green-300 bg-green-50">

**Conviene**

Un equipo que ya sabe React y necesita una app para iOS y Android con un único código fuente, sin mantener dos equipos nativos separados.

</div>
<div class="p-4 rounded-lg border-2 border-yellow-300 bg-yellow-50">

**Pensarlo dos veces**

Una app que depende fuerte de una API nativa muy específica y reciente de una sola plataforma, o con requisitos extremos de rendimiento (juegos 3D) donde nativo puro sigue siendo la opción más directa.

</div>
</div>

<div class="mt-3 text-sm italic opacity-80 text-center">

Para la enorme mayoría de apps de negocio (listas, formularios, APIs), la diferencia de rendimiento contra nativo puro no se nota.

</div>

---
layout: default
---

# Cheat sheet

<div class="grid grid-cols-2 gap-8 mt-2 text-xs">
<div>

**Componentes básicos**

| Web | React Native |
|---|---|
| `<div>` | `<View>` |
| texto suelto | `<Text>` |
| `<button onClick>` | `<Pressable onPress>` |
| `.map()` en una lista | `<FlatList>` |
| CSS | `StyleSheet.create({...})` |

</div>
<div>

**Comandos**

| Comando | Para qué |
|---|---|
| `create-expo-app` | Crear proyecto |
| `expo start` | Servidor de desarrollo |
| `expo install <pkg>` | Instalar compatible |
| `eas build` | Compilar en la nube |
| `eas update` | Publicar JS sin store |

</div>
</div>

---
layout: default
---

# Referencias y recursos

<div class="space-y-2 mt-2 text-sm">

- [docs.expo.dev](https://docs.expo.dev) — documentación oficial
- [docs.expo.dev/get-started/create-a-project](https://docs.expo.dev/get-started/create-a-project/) — instalación y primer proyecto
- [docs.expo.dev/router/introduction](https://docs.expo.dev/router/introduction/) — Expo Router, en profundidad
- [reactnative.dev/docs/components-and-apis](https://reactnative.dev/docs/components-and-apis) — todos los componentes nativos
- [reactnative.dev/docs/flexbox](https://reactnative.dev/docs/flexbox) — flexbox en React Native (diferencias con CSS web)
- [docs.expo.dev/versions/latest](https://docs.expo.dev/versions/latest/) — todos los paquetes `expo-*` disponibles
- [docs.expo.dev/build/introduction](https://docs.expo.dev/build/introduction/) — EAS Build
- [docs.expo.dev/eas-update/introduction](https://docs.expo.dev/eas-update/introduction/) — EAS Update (OTA)
- [snack.expo.dev](https://snack.expo.dev) — playground oficial, corre en el teléfono sin instalar nada
- [docs.expo.dev/tutorial/introduction](https://docs.expo.dev/tutorial/introduction/) — tutorial guiado oficial

</div>
