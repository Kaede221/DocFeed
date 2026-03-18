<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getFrameworks, generateContext } from './api'
import type { FrameworkInfo, GenerateResponse } from './types'

// --- state ---
const frameworks = ref<FrameworkInfo[]>([])
const selectedFrameworkId = ref('')
const selectedModules = ref<Set<string>>(new Set())
const loading = ref(false)
const loadingFrameworks = ref(false)
const result = ref<GenerateResponse | null>(null)
const copied = ref(false)
const error = ref('')

// --- computed ---
const currentFramework = computed(() =>
  frameworks.value.find((f) => f.id === selectedFrameworkId.value),
)

const canGenerate = computed(() => selectedFrameworkId.value && selectedModules.value.size > 0)

// --- actions ---
onMounted(async () => {
  loadingFrameworks.value = true
  try {
    frameworks.value = await getFrameworks()
    if (frameworks.value.length > 0) {
      selectedFrameworkId.value = frameworks.value[0].id
    }
  } catch (e: any) {
    error.value = 'Failed to load frameworks: ' + (e.message || e)
  } finally {
    loadingFrameworks.value = false
  }
})

function onFrameworkChange() {
  selectedModules.value = new Set()
  result.value = null
  error.value = ''
}

function toggleModule(path: string) {
  const next = new Set(selectedModules.value)
  if (next.has(path)) {
    next.delete(path)
  } else {
    next.add(path)
  }
  selectedModules.value = next
}

function selectAllModules() {
  if (!currentFramework.value) return
  const allPaths = currentFramework.value.modules.map((m) => m.path)
  if (selectedModules.value.size === allPaths.length) {
    selectedModules.value = new Set()
  } else {
    selectedModules.value = new Set(allPaths)
  }
}

async function generate() {
  if (!canGenerate.value) return
  loading.value = true
  error.value = ''
  result.value = null
  try {
    result.value = await generateContext({
      framework_id: selectedFrameworkId.value,
      module_paths: [...selectedModules.value],
    })
  } catch (e: any) {
    error.value = 'Failed to generate context: ' + (e.message || e)
  } finally {
    loading.value = false
  }
}

async function copyToClipboard() {
  if (!result.value) return
  await navigator.clipboard.writeText(result.value.context)
  copied.value = true
  setTimeout(() => (copied.value = false), 2000)
}
</script>

<template>
  <div class="container">
    <!-- Header -->
    <header class="header">
      <h1>DocFeed</h1>
      <p class="tagline">Feed your AI the freshest docs.</p>
    </header>

    <!-- Loading state -->
    <div v-if="loadingFrameworks" class="loading-card">Loading frameworks...</div>

    <template v-else>
      <!-- Step 1: Select Framework -->
      <section class="card">
        <h2>1. Select Framework</h2>
        <div class="framework-tabs">
          <button
            v-for="fw in frameworks"
            :key="fw.id"
            :class="['tab', { active: selectedFrameworkId === fw.id }]"
            @click="selectedFrameworkId = fw.id; onFrameworkChange()"
          >
            {{ fw.name }}
          </button>
        </div>
      </section>

      <!-- Step 2: Select Modules -->
      <section v-if="currentFramework" class="card">
        <div class="card-header">
          <h2>2. Select Modules</h2>
          <button class="link-btn" @click="selectAllModules">
            {{
              selectedModules.size === currentFramework.modules.length
                ? 'Deselect All'
                : 'Select All'
            }}
          </button>
        </div>
        <div class="module-grid">
          <label
            v-for="mod in currentFramework.modules"
            :key="mod.path"
            :class="['module-item', { selected: selectedModules.has(mod.path) }]"
          >
            <input
              type="checkbox"
              :checked="selectedModules.has(mod.path)"
              @change="toggleModule(mod.path)"
            />
            <span>{{ mod.label }}</span>
          </label>
        </div>
      </section>

      <!-- Generate Button -->
      <button class="generate-btn" :disabled="!canGenerate || loading" @click="generate">
        {{ loading ? 'Generating...' : 'Generate Context' }}
      </button>

      <!-- Error -->
      <div v-if="error" class="error">{{ error }}</div>

      <!-- Result -->
      <section v-if="result" class="card result-card">
        <div class="card-header">
          <h2>Generated Context</h2>
          <button class="copy-btn" @click="copyToClipboard">
            {{ copied ? 'Copied!' : 'Copy to Clipboard' }}
          </button>
        </div>
        <div class="result-stats">
          <span>{{ result.framework }}</span>
          <span>{{ result.file_count }} files</span>
          <span>{{ (result.char_count / 1024).toFixed(1) }} KB</span>
        </div>
        <pre class="result-content">{{ result.context }}</pre>
      </section>
    </template>
  </div>
</template>