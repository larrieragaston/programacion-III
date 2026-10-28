---
theme: bricks
title: Programación III - NestJS
download: true
info: |
  NestJS - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: nestjs, nodejs, typescript, decoradores, inyección de dependencias, backend, INSPT, UTN
transition: slide-left
mdc: true
---

# NestJS

Programación III

<div class="flex gap-8 justify-end mr-16 mt-6 items-center">
<img src="/logos/nestjs.svg" alt="NestJS" class="h-14 opacity-90" />
</div>

<div class="abs-b mb-8 text-sm opacity-60">
INSPT - UTN · Ciclo Lectivo 2026
</div>

---
layout: default
---

# ¿Qué es NestJS?

- Un framework para construir backends en Node, con **TypeScript** como lenguaje de primera clase (no un agregado opcional).
- Corre arriba de un framework HTTP existente (Express por defecto, o Fastify) — no reemplaza esa capa, le agrega **estructura**: cómo organizar rutas, lógica de negocio y dependencias en piezas con un rol claro.
- Usa **decoradores** (`@Controller()`, `@Injectable()`) para describir esa estructura — leídos en tiempo de ejecución para armar la aplicación automáticamente.

<div class="flex gap-10 justify-center mt-6 items-center">
<img src="/logos/nestjs.svg" alt="NestJS" class="h-12 opacity-80" />
</div>

---
layout: default
---

# Historia breve

- **2017** — Kamil Myśliwiec lo libera, inspirado explícitamente en la arquitectura de **Angular**: módulos, inyección de dependencias, decoradores — ideas ya probadas del lado del frontend, aplicadas al backend.
- **2019** (v6) — soporte oficial para **Fastify** como alternativa a Express, sin cambiar el código de la aplicación.
- **2023** (v10) — mejoras de rendimiento y compatibilidad con Node 20.
- **2026** (v11/v12) — reemplazo del tooling: **SWC** para compilar más rápido, **Vitest** en vez de Jest, módulos **ESM** por defecto en proyectos nuevos.
- **Hoy** — uno de los frameworks backend de Node más usados en equipos que ya vienen de TypeScript, por lo predecible de su estructura.

---
layout: center
---

# Empezar un proyecto

---
layout: default
---

# Nest CLI: crear un proyecto

```bash
npm install -g @nestjs/cli
nest new mi-api
```

<div class="mt-3 text-sm opacity-80">

Pregunta el gestor de paquetes y arma un proyecto corriendo (`npm run start:dev`) con un módulo, un controlador y un servicio de ejemplo — el "Hello World" del framework. Todo el código generado por el CLI en este apunte usa TypeScript con módulos ESM (import/export nativos), el default en proyectos nuevos.

</div>

<div class="mt-1 text-xs opacity-60">

→ [docs.nestjs.com/first-steps](https://docs.nestjs.com/first-steps)

</div>

---
layout: default
---

# Estructura del proyecto

<div class="grid grid-cols-2 gap-3 text-sm">
<div>

```
mi-api/
├── src/
│   ├── app.module.ts
│   ├── app.controller.ts
│   ├── app.service.ts
│   └── main.ts
├── test/
└── nest-cli.json
```

</div>
<div>

```ts
// src/main.ts
import { NestFactory } from '@nestjs/core'
import { AppModule } from './app.module.js'

async function bootstrap() {
  const app = await NestFactory.create(AppModule)
  await app.listen(process.env.PORT ?? 3000)
}
await bootstrap()
```

</div>
</div>

<div class="mt-1 text-xs opacity-80">

`NestFactory.create` arma toda la aplicación a partir de un único módulo raíz — el resto de los módulos se conectan a partir de ahí, por `import`.

</div>

---
layout: center
---

# Los tres bloques básicos

---
layout: default
---

# Módulos

```ts
// products.module.ts
import { Module } from '@nestjs/common'
import { ProductsController } from './products.controller.js'
import { ProductsService } from './products.service.js'

@Module({
  controllers: [ProductsController],
  providers: [ProductsService],
})
export class ProductsModule {}
```

<div class="mt-2 text-sm opacity-80">

Un módulo agrupa todo lo relacionado a una parte del dominio (`products`, `users`, `orders`) — qué controladores expone y qué providers usa. `AppModule` (el raíz) importa los módulos de cada feature, armando el árbol completo de la aplicación.

</div>

---
layout: default
---

# Controladores

```ts
import { Controller, Get, Param } from '@nestjs/common'
import { ProductsService } from './products.service.js'

@Controller('products')
export class ProductsController {
  constructor(private readonly productsService: ProductsService) {}
  @Get()
  findAll() {
    return this.productsService.findAll()
  }
  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.productsService.findOne(+id)
  }
}
```

<div class="mt-1 text-xs opacity-80">

`@Controller('products')` fija el prefijo de ruta; `@Get()`/`@Post()` el método HTTP. El controlador solo orquesta: delega la lógica al service.

</div>

---
layout: default
---

# Providers y servicios

```ts
import { Injectable, NotFoundException } from '@nestjs/common'

@Injectable()
export class ProductsService {
  private products = []
  findAll() {
    return this.products
  }
  findOne(id: number) {
    const product = this.products.find((p) => p.id === id)
    if (!product) throw new NotFoundException(`Product ${id} not found`)
    return product
  }
}
```

<div class="mt-2 text-sm opacity-80">

`@Injectable()` marca una clase como **provider** — algo que Nest puede crear e inyectar donde haga falta. Acá vive la lógica de negocio real, separada del detalle de "es una ruta HTTP" que maneja el controlador.

</div>

---
layout: default
---

# Inyección de dependencias

```ts
@Controller('products')
export class ProductsController {
  constructor(private readonly productsService: ProductsService) {}
  // ...
}
```

<div class="mt-3 text-sm opacity-80">

El controlador nunca hace `new ProductsService()` — solo lo pide en el constructor, tipado. Nest tiene un contenedor (*IoC container*) que ve ese tipo, busca (o crea) una instancia de `ProductsService` ya registrada en el módulo, y se la pasa automáticamente. La ventaja aparece al testear: en un test se puede inyectar una versión falsa del service, sin tocar el controlador.

</div>

---
layout: center
---

# Generar código con el CLI

---
layout: default
---

# `nest generate`

```bash
nest g module products      # o: nest g mo products
nest g controller products  # o: nest g co products
nest g service products     # o: nest g s products

# o las tres juntas, con DTOs y entidad de una vez:
nest g resource products
```

<div class="mt-2 text-sm opacity-80">

`resource` pregunta qué transporte usar (REST, GraphQL, microservicios...) y arma el CRUD completo: controlador con las 5 rutas (`GET`, `GET :id`, `POST`, `PATCH`, `DELETE`), service con los métodos correspondientes, módulo que los conecta, y DTOs de `create`/`update` vacíos, listos para completar.

</div>

<div class="mt-1 text-xs opacity-60">

→ [docs.nestjs.com/cli/usages](https://docs.nestjs.com/cli/usages)

</div>

---
layout: center
---

# Validar datos

---
layout: default
---

# DTOs

```ts
// dto/create-product.dto.ts
export class CreateProductDto {}
```

<div class="mt-3 text-sm opacity-80">

Un *Data Transfer Object*: una clase que describe la forma de los datos que entran por una ruta — qué espera recibir un `POST`, qué un `PATCH`. El CLI los genera vacíos; el siguiente paso es agregarles **validación real**, no solo tipos de TypeScript (que desaparecen en tiempo de ejecución).

</div>

---
layout: default
---

# Validación con `class-validator`

```bash
npm install class-validator class-transformer
```

<div class="grid grid-cols-2 gap-3 text-sm mt-2">
<div>

```ts
// dto/create-product.dto.ts
import {
  IsString, IsNotEmpty, IsNumber, Min,
} from 'class-validator'

export class CreateProductDto {
  @IsString()
  @IsNotEmpty()
  name: string
  @IsNumber()
  @Min(0)
  price: number
}
```

</div>
<div>

```ts
// main.ts
app.useGlobalPipes(
  new ValidationPipe({ whitelist: true })
)
```

<div class="mt-2 text-xs opacity-80">

Los decoradores de `class-validator` describen las reglas sobre el DTO. `ValidationPipe`, activado global, valida el body **antes** de llegar al controlador — si falla, devuelve `400` solo. `whitelist: true` descarta campos no declarados.

</div>

</div>
</div>

---
layout: center
---

# CRUD completo

---
layout: default
---

# El recurso completo

```ts
@Injectable()
export class ProductsService {
  private products: Product[] = []
  private nextId = 1
  create(dto: CreateProductDto): Product {
    const product = { id: this.nextId++, ...dto }
    this.products.push(product)
    return product
  }
  findOne(id: number): Product {
    const product = this.products.find((p) => p.id === id)
    if (!product) throw new NotFoundException(`Product ${id} not found`)
    return product
  }
}
```

<div class="mt-1 text-xs opacity-80">

El controlador ya visto alcanza para exponer esto — solo le faltaba un `@Post()` con `@Body() dto: CreateProductDto` para llegar al `create`.

</div>

---
layout: default
---

# Probar con `curl`

```bash
curl -X POST localhost:3000/products -H 'Content-Type: application/json' \
  -d '{"name":"Mouse","price":1500}'
# → 201 {"id":1,"name":"Mouse","price":1500}

curl -X POST localhost:3000/products -H 'Content-Type: application/json' \
  -d '{"name":"","price":-5}'
# → 400 {"message":["name should not be empty","price must not be less than 0"], ...}

curl localhost:3000/products/999
# → 404 {"message":"Product 999 not found", ...}
```

<div class="mt-2 text-sm opacity-80">

Tres respuestas, ninguna escrita a mano en el controlador: la validación del DTO arma el `400`, y `NotFoundException` arma el `404` — Nest se encarga de convertir esas excepciones en la respuesta HTTP correcta.

</div>

---
layout: center
---

# Proteger rutas

---
layout: default
---

# Guards: qué son

- Una clase que decide, **antes** de que una request llegue al controlador, si puede pasar o no — autenticación, permisos, lo que sea una condición de sí/no.
- Implementan `CanActivate`: un método `canActivate()` que devuelve (o resuelve a) `true` o `false` — o tira una excepción para dar un mensaje más específico que un simple rechazo.
- Se activan con `@UseGuards(...)`, a nivel de una ruta, de todo un controlador, o global para toda la aplicación.

---
layout: default
---

# Un guard de ejemplo

<div class="grid grid-cols-2 gap-3 text-sm">
<div>

```ts
// api-key.guard.ts
@Injectable()
export class ApiKeyGuard
  implements CanActivate {
  canActivate(ctx: ExecutionContext): boolean {
    const req = ctx.switchToHttp().getRequest<Request>()
    const apiKey = req.headers['x-api-key']
    if (apiKey !== process.env.API_KEY) {
      throw new UnauthorizedException('Inválida')
    }
    return true
  }
}
```

</div>
<div>

```ts
@UseGuards(ApiKeyGuard)
@Post()
create(@Body() dto: CreateProductDto) {
  return this.productsService.create(dto)
}
```

<div class="mt-2 text-xs opacity-80">

`ExecutionContext` da acceso al request HTTP real — desde ahí, la lógica es código común.

</div>

</div>
</div>

---
layout: center
---

# Más piezas del pipeline

---
layout: default
---

# Pipes, interceptors y filters

<div class="grid grid-cols-3 gap-3 mt-3 text-sm">
<div class="p-3 rounded-lg border border-blue-300 bg-blue-50">
<strong>Pipes</strong><br/>
Transforman o validan datos de entrada antes de que lleguen al método (<code>ValidationPipe</code>, o convertir un <code>:id</code> de string a number).
</div>
<div class="p-3 rounded-lg border border-purple-300 bg-purple-50">
<strong>Interceptors</strong><br/>
Envuelven la ejecución del método — pueden transformar la respuesta, medir tiempos, o cachear, corriendo antes <strong>y</strong> después.
</div>
<div class="p-3 rounded-lg border border-red-300 bg-red-50">
<strong>Exception filters</strong><br/>
Capturan una excepción no manejada y deciden qué responder — <code>NotFoundException</code> ya usa uno incorporado.
</div>
</div>

<div class="mt-4 text-sm opacity-80">

Los cuatro (guards incluidos) son el mismo patrón: una clase chica, con una responsabilidad, que se activa con un decorador — en una ruta, un controlador, o toda la app.

</div>

<div class="mt-1 text-xs opacity-60">

→ [docs.nestjs.com/pipes](https://docs.nestjs.com/pipes) · [docs.nestjs.com/interceptors](https://docs.nestjs.com/interceptors) · [docs.nestjs.com/exception-filters](https://docs.nestjs.com/exception-filters)

</div>

---
layout: center
---

# Persistencia

---
layout: default
---

# Conectar una base de datos

```bash
npm install @nestjs/typeorm typeorm better-sqlite3
```

<div class="grid grid-cols-2 gap-3 text-sm mt-2">
<div>

```ts
// product.entity.ts
@Entity()
export class Product {
  @PrimaryGeneratedColumn()
  id: number
  @Column()
  name: string
}
```

</div>
<div>

```ts
// products.module.ts
@Module({
  imports: [TypeOrmModule.forFeature([Product])],
  providers: [ProductsService],
})
export class ProductsModule {}
```

</div>
</div>

<div class="mt-2 text-xs opacity-80">

**TypeORM** (decoradores sobre entidades) y **Prisma** (schema propio + cliente generado) son las opciones más comunes — ambas se conectan como un módulo más. El service pide un `Repository<Product>` por inyección de dependencias, como cualquier provider.

</div>

---
layout: default
---

# Usar el repositorio

```ts
@Injectable()
export class ProductsService {
  constructor(
    @InjectRepository(Product)
    private readonly repo: Repository<Product>,
  ) {}
  create(data: Partial<Product>) {
    return this.repo.save(this.repo.create(data))
  }
  findAll() {
    return this.repo.find()
  }
}
```

<div class="mt-2 text-sm opacity-80">

`@InjectRepository(Product)` le pide a Nest el repositorio de esa entidad, ya configurado — mismo mecanismo de inyección que un service común, ahora para acceso a datos.

</div>

---
layout: center
---

# Testing

---
layout: default
---

# Testing en NestJS

```ts
import { Test } from '@nestjs/testing'

describe('ProductsService', () => {
  it('crea y lista productos', async () => {
    const moduleRef = await Test.createTestingModule({
      providers: [ProductsService],
    }).compile()
    const service = moduleRef.get(ProductsService)
    await service.create({ name: 'Mouse', price: 1500 })

    expect(await service.findAll()).toHaveLength(1)
  })
})
```

<div class="mt-1 text-xs opacity-80">

`Test.createTestingModule` arma un módulo de Nest real solo para el test — con la misma inyección de dependencias de la app, pudiendo reemplazar cualquier provider por uno falso (`overrideProvider`). Desde la v11, el CLI escafolda con **Vitest** en vez de Jest por defecto, aunque ambos funcionan igual con este patrón.

</div>

---
layout: center
---

# Cierre

---
layout: default
---

# ¿Cuándo conviene NestJS?

<div class="grid grid-cols-2 gap-6 mt-2">
<div class="p-4 rounded-lg border-2 border-green-300 bg-green-50">

**Conviene**

Un backend que va a crecer en equipo, con muchos módulos y necesidad de una estructura compartida y predecible — o un equipo que ya viene de Angular y reconoce el patrón.

</div>
<div class="p-4 rounded-lg border-2 border-yellow-300 bg-yellow-50">

**Pensarlo dos veces**

Una API chica, de pocas rutas, donde armar módulos/providers es más ceremonia de la que el proyecto necesita — ahí un framework más minimalista alcanza y sobra.

</div>
</div>

<div class="mt-3 text-sm italic opacity-80 text-center">

La estructura que impone tiene un costo de entrada — se paga sola en proyectos que de verdad la necesitan.

</div>

---
layout: default
---

# Cheat sheet

<div class="grid grid-cols-2 gap-8 mt-2 text-xs">
<div>

**Piezas básicas**

| Decorador | Para qué |
|---|---|
| `@Module({...})` | Agrupar controllers/providers |
| `@Controller('ruta')` | Definir rutas |
| `@Get()` / `@Post()` / ... | Método HTTP |
| `@Injectable()` | Marcar un provider |
| `@Body()` / `@Param()` | Leer datos del request |

</div>
<div>

**CLI y pipeline**

| Comando/decorador | Para qué |
|---|---|
| `nest g resource x` | CRUD completo |
| `@UseGuards(G)` | Proteger una ruta |
| `ValidationPipe` | Validar DTOs |
| `@InjectRepository(E)` | Repositorio de una entidad |
| `Test.createTestingModule` | Testear con DI real |

</div>
</div>

---
layout: default
---

# Referencias y recursos

<div class="space-y-2 mt-2 text-sm">

- [docs.nestjs.com](https://docs.nestjs.com) — documentación oficial
- [docs.nestjs.com/first-steps](https://docs.nestjs.com/first-steps) — instalación y estructura inicial
- [docs.nestjs.com/controllers](https://docs.nestjs.com/controllers) — controladores y rutas, en profundidad
- [docs.nestjs.com/providers](https://docs.nestjs.com/providers) — providers e inyección de dependencias
- [docs.nestjs.com/techniques/validation](https://docs.nestjs.com/techniques/validation) — DTOs y `class-validator`
- [docs.nestjs.com/guards](https://docs.nestjs.com/guards) — guards y autenticación
- [docs.nestjs.com/pipes](https://docs.nestjs.com/pipes) — pipes, interceptors y exception filters
- [docs.nestjs.com/recipes/sql-typeorm](https://docs.nestjs.com/recipes/sql-typeorm) — integración con TypeORM
- [docs.nestjs.com/fundamentals/testing](https://docs.nestjs.com/fundamentals/testing) — testing con `@nestjs/testing`
- [docs.nestjs.com/cli/usages](https://docs.nestjs.com/cli/usages) — todos los comandos del CLI

</div>
