<template>
  <div class="dataset-explorer">
    <!-- Controls bar -->
    <div class="controls">
      <input
        v-model="searchQuery"
        class="search-input"
        placeholder="Search by name, sector, category…"
        type="search"
      />
      <select v-model="filterSector" class="filter-select">
        <option value="">All Sectors</option>
        <option v-for="s in sectorOptions" :key="s" :value="s">{{ s }}</option>
      </select>
      <select v-model="filterGovernance" class="filter-select">
        <option value="">All Governance Types</option>
        <option v-for="g in governanceOptions" :key="g" :value="g">{{ g }}</option>
      </select>
      <select v-model="filterDecentralisation" class="filter-select">
        <option value="">All Decentralisation Levels</option>
        <option v-for="d in decentralisationOptions" :key="d" :value="d">{{ d }}</option>
      </select>
      <button class="reset-btn" @click="resetFilters">Reset</button>
    </div>

    <!-- Stats row -->
    <div class="stats-row">
      Showing <strong>{{ filteredRows.length }}</strong> of <strong>{{ rows.length }}</strong> DApps
      <span v-if="totalPages > 1"> · Page {{ currentPage }} / {{ totalPages }}</span>
    </div>

    <!-- Table -->
    <div class="table-wrapper">
      <table class="dataset-table" v-if="pagedRows.length > 0">
        <thead>
          <tr>
            <th v-for="col in visibleColumns" :key="col" @click="sortBy(col)" class="sortable-th">
              {{ formatHeader(col) }}
              <span v-if="sortColumn === col">{{ sortAsc ? '▲' : '▼' }}</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, idx) in pagedRows" :key="idx">
            <td v-for="col in visibleColumns" :key="col" :class="cellClass(col, row[col])">
              <template v-if="col === 'website' && row[col]">
                <a :href="row[col]" target="_blank" rel="noopener noreferrer">↗</a>
              </template>
              <template v-else>{{ row[col] || '—' }}</template>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="no-results">No DApps match the current filters.</div>
    </div>

    <!-- Pagination -->
    <div class="pagination" v-if="totalPages > 1">
      <button :disabled="currentPage === 1" @click="currentPage--">‹ Prev</button>
      <span>Page {{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="currentPage++">Next ›</button>
    </div>

    <!-- Column toggle -->
    <details class="column-toggle">
      <summary>Toggle columns</summary>
      <div class="column-checkboxes">
        <label v-for="col in allColumns" :key="col">
          <input type="checkbox" :value="col" v-model="visibleColumns" /> {{ formatHeader(col) }}
        </label>
      </div>
    </details>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

interface DataRow {
  [key: string]: string
}

const rows = ref<DataRow[]>([])
const allColumns = ref<string[]>([])
const loading = ref(true)

const DEFAULT_COLUMNS = [
  'name', 'dapp_sector', 'dapp_category', 'governance_type',
  'ownership_status', 'level_of_decentralisation', 'token_symbol',
  'token_type', 'chains', 'tvl', 'market_cap', 'users', 'website'
]

const visibleColumns = ref<string[]>(DEFAULT_COLUMNS)
const searchQuery = ref('')
const filterSector = ref('')
const filterGovernance = ref('')
const filterDecentralisation = ref('')
const sortColumn = ref('')
const sortAsc = ref(true)
const currentPage = ref(1)
const PAGE_SIZE = 50

onMounted(async () => {
  try {
    const res = await fetch('/dapp-dataset.json')
    const data = await res.json()
    rows.value = data.rows
    allColumns.value = data.headers
    // Ensure visible columns are valid
    visibleColumns.value = DEFAULT_COLUMNS.filter(c => data.headers.includes(c))
  } finally {
    loading.value = false
  }
})

const sectorOptions = computed(() =>
  [...new Set(rows.value.map(r => r.dapp_sector).filter(Boolean))].sort()
)
const governanceOptions = computed(() =>
  [...new Set(rows.value.map(r => r.governance_type).filter(Boolean))].sort()
)
const decentralisationOptions = computed(() =>
  [...new Set(rows.value.map(r => r.level_of_decentralisation).filter(Boolean))].sort()
)

const filteredRows = computed(() => {
  let result = rows.value
  const q = searchQuery.value.toLowerCase().trim()
  if (q) {
    result = result.filter(r =>
      r.name?.toLowerCase().includes(q) ||
      r.dapp_sector?.toLowerCase().includes(q) ||
      r.dapp_category?.toLowerCase().includes(q) ||
      r.sub_category?.toLowerCase().includes(q) ||
      r.token_symbol?.toLowerCase().includes(q) ||
      r.chains?.toLowerCase().includes(q)
    )
  }
  if (filterSector.value) result = result.filter(r => r.dapp_sector === filterSector.value)
  if (filterGovernance.value) result = result.filter(r => r.governance_type === filterGovernance.value)
  if (filterDecentralisation.value) result = result.filter(r => r.level_of_decentralisation === filterDecentralisation.value)

  if (sortColumn.value) {
    const col = sortColumn.value
    result = [...result].sort((a, b) => {
      const av = a[col] || ''
      const bv = b[col] || ''
      const numA = parseFloat(av), numB = parseFloat(bv)
      if (!isNaN(numA) && !isNaN(numB)) return sortAsc.value ? numA - numB : numB - numA
      return sortAsc.value ? av.localeCompare(bv) : bv.localeCompare(av)
    })
  }
  return result
})

const totalPages = computed(() => Math.ceil(filteredRows.value.length / PAGE_SIZE))

const pagedRows = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filteredRows.value.slice(start, start + PAGE_SIZE)
})

watch(filteredRows, () => { currentPage.value = 1 })

function sortBy(col: string) {
  if (sortColumn.value === col) sortAsc.value = !sortAsc.value
  else { sortColumn.value = col; sortAsc.value = true }
}

function resetFilters() {
  searchQuery.value = ''
  filterSector.value = ''
  filterGovernance.value = ''
  filterDecentralisation.value = ''
  sortColumn.value = ''
  sortAsc.value = true
  currentPage.value = 1
}

function formatHeader(col: string): string {
  return col.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}

function cellClass(col: string, val: string): string {
  if (col === 'level_of_decentralisation') {
    if (val === 'DECENTRALIZED') return 'badge badge-green'
    if (val === 'SEMI_DECENTRALIZED') return 'badge badge-yellow'
    if (val === 'CENTRALIZED') return 'badge badge-red'
  }
  if (col === 'is_active') return val === 'TRUE' ? 'badge badge-green' : 'badge badge-red'
  return ''
}
</script>

<style scoped>
.dataset-explorer { font-size: 0.9rem; }

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.search-input {
  flex: 1 1 200px;
  padding: 0.4rem 0.6rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 0.9rem;
}

.filter-select {
  padding: 0.4rem 0.6rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 0.85rem;
}

.reset-btn {
  padding: 0.4rem 0.9rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  cursor: pointer;
  font-size: 0.85rem;
}
.reset-btn:hover { background: var(--vp-c-bg-mute); }

.stats-row {
  margin-bottom: 0.5rem;
  color: var(--vp-c-text-2);
  font-size: 0.85rem;
}

.table-wrapper {
  overflow-x: auto;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
}

.dataset-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
}

.dataset-table th, .dataset-table td {
  padding: 0.4rem 0.6rem;
  border-bottom: 1px solid var(--vp-c-divider);
  white-space: nowrap;
  max-width: 220px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dataset-table th {
  background: var(--vp-c-bg-soft);
  font-weight: 600;
  text-align: left;
  position: sticky;
  top: 0;
  z-index: 1;
}

.sortable-th { cursor: pointer; user-select: none; }
.sortable-th:hover { background: var(--vp-c-bg-mute); }

.dataset-table tr:last-child td { border-bottom: none; }
.dataset-table tbody tr:hover { background: var(--vp-c-bg-soft); }

.no-results {
  padding: 2rem;
  text-align: center;
  color: var(--vp-c-text-2);
}

.badge { display: inline-block; padding: 0.1rem 0.4rem; border-radius: 4px; font-size: 0.75rem; }
.badge-green { background: #d1fae5; color: #065f46; }
.badge-yellow { background: #fef3c7; color: #92400e; }
.badge-red { background: #fee2e2; color: #991b1b; }

:global(.dark) .badge-green { background: #064e3b; color: #6ee7b7; }
:global(.dark) .badge-yellow { background: #78350f; color: #fcd34d; }
:global(.dark) .badge-red { background: #7f1d1d; color: #fca5a5; }

.pagination {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.75rem;
  font-size: 0.85rem;
}
.pagination button {
  padding: 0.3rem 0.8rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  cursor: pointer;
}
.pagination button:disabled { opacity: 0.4; cursor: not-allowed; }
.pagination button:not(:disabled):hover { background: var(--vp-c-bg-mute); }

.column-toggle {
  margin-top: 1rem;
  font-size: 0.85rem;
}
.column-toggle summary { cursor: pointer; color: var(--vp-c-brand); }
.column-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem 1rem;
  margin-top: 0.5rem;
}
.column-checkboxes label { display: flex; align-items: center; gap: 0.3rem; }
</style>
