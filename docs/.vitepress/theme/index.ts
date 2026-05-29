import DefaultTheme from 'vitepress/theme'
import DataTable from './DataTable.vue'
import type { Theme } from 'vitepress'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('DataTable', DataTable)
  },
} satisfies Theme
