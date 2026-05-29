import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'DApp Thesis — Politecnico di Milano',
  description: "Master's Thesis: Decentralised Applications in Focus — Governance, Market Structure, and Adoption Patterns",

  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Thesis', link: '/thesis/' },
      { text: 'Analytics', link: '/analytics/' },
      { text: 'Datasets', link: '/datasets/' },
      { text: 'Appendices', link: '/appendices/variable-codebook' },
      { text: 'References', link: '/reference-docs' },
    ],

    sidebar: {
      '/thesis/': [
        {
          text: 'Thesis Chapters',
          items: [
            { text: 'Overview', link: '/thesis/' },
            { text: 'Abstract', link: '/thesis/abstract' },
            { text: '1. Introduction', link: '/thesis/01-introduction' },
            { text: '2. Literature Review', link: '/thesis/02-literature-review' },
            { text: '3. Methodology', link: '/thesis/03-methodology' },
            { text: '4. Results', link: '/thesis/04-results' },
            { text: '4c. Case Studies', link: '/thesis/04c-case-studies' },
            { text: '5. Discussion', link: '/thesis/05-discussion' },
            { text: '6. Conclusions', link: '/thesis/06-conclusions' },
            { text: 'References', link: '/thesis/references' },
            { text: 'Review Feedback', link: '/thesis/review-feedback' },
          ],
        },
      ],
      '/analytics/': [
        {
          text: 'Analytics',
          items: [
            { text: 'Overview', link: '/analytics/' },
          ],
        },
        {
          text: 'Original Analysis',
          items: [
            { text: 'Overview', link: '/analytics/original/' },
            { text: 'Summary', link: '/analytics/original/summary' },
            { text: 'Completion Report', link: '/analytics/original/completion' },
            { text: 'Presentation', link: '/analytics/original/presentation' },
          ],
        },
        {
          text: 'Merged Analysis',
          items: [
            { text: 'Overview', link: '/analytics/merged/' },
            { text: 'Methodology', link: '/analytics/merged/methodology' },
            { text: 'Results & Discussion', link: '/analytics/merged/results' },
            { text: 'Key Insights', link: '/analytics/merged/insights' },
            { text: 'Anomalies', link: '/analytics/merged/anomalies' },
            { text: 'Thesis Brief', link: '/analytics/merged/brief' },
          ],
        },
        {
          text: 'Latest Analysis',
          items: [
            { text: 'Overview', link: '/analytics/latest/' },
            { text: 'Methodology', link: '/analytics/latest/methodology' },
            { text: 'Results & Discussion', link: '/analytics/latest/results' },
            { text: 'Key Insights', link: '/analytics/latest/insights' },
            { text: 'Anomalies', link: '/analytics/latest/anomalies' },
            { text: 'Thesis Brief', link: '/analytics/latest/brief' },
          ],
        },
      ],
      '/datasets/': [
        {
          text: 'Datasets',
          items: [
            { text: 'Dataset Inventory', link: '/datasets/' },
          ],
        },
      ],
      '/appendices/': [
        {
          text: 'Appendices',
          items: [
            { text: 'Appendix A: Variable Codebook', link: '/appendices/variable-codebook' },
            { text: 'Appendix B: Analytical Pipeline', link: '/appendices/analytical-pipeline' },
          ],
        },
      ],
    },

    search: {
      provider: 'local',
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/krislander/dapp-scaner' },
    ],

    footer: {
      message: 'MSc Thesis — Politecnico di Milano, Academic Year 2024–2025',
      copyright: 'Decentralised Applications in Focus: Governance, Market Structure, and Adoption Patterns',
    },
  },
})
