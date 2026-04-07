<template>
  <a
    v-if="!isPrintMode"
    class="home-link"
    :href="homeHref"
    title="Volver al índice"
    aria-label="Volver al índice principal"
  >
    <svg aria-hidden="true" viewBox="0 0 24 24" class="home-icon">
      <path d="M3 11.5 12 4l9 7.5" />
      <path d="M5 10.5V20h14v-9.5" />
      <path d="M10 20v-5h4v5" />
    </svg>
  </a>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const isPrintMode = computed(
  () => 'print' in route.query || route.name === 'export',
)

const homeHref = computed(() => {
  if (typeof window === 'undefined') return '/programacion-III/'

  const { protocol, hostname, pathname } = window.location

  if (hostname === 'localhost' || hostname === '127.0.0.1')
    return `${protocol}//${hostname}:3030/`

  if (pathname.startsWith('/programacion-III/')) return '/programacion-III/'

  return '/'
})
</script>

<style scoped>
.home-link {
  position: fixed;
  top: 0.8rem;
  right: 0.8rem;
  z-index: 60;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 0.55rem;
  background: rgba(255, 255, 255, 0.95);
  color: #111827;
  text-decoration: none;
  font-size: 1rem;
  line-height: 1;
  border: 1px solid rgba(15, 23, 42, 0.14);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
  backdrop-filter: blur(2px);
  transition: background-color 120ms ease, border-color 120ms ease, box-shadow 120ms ease;
}

.home-icon {
  width: 1.05rem;
  height: 1.05rem;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.9;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.home-link:hover {
  background: #ffffff;
  border-color: rgba(15, 23, 42, 0.24);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.12);
}

.home-link:focus-visible {
  outline: 2px solid #60a5fa;
  outline-offset: 2px;
}
</style>
