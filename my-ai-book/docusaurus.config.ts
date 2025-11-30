import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  // 1. PROJECT DETAILS
  title: 'Agentic AI Book', 
  tagline: 'Generated via Claude Code & Spec-Kit',
  favicon: 'img/favicon.ico',

  // 2. GITHUB PAGES DEPLOYMENT CONFIG (CRITICAL)
  url: 'https://raza-ahmed-khan360.github.io', // Your User Domain
  baseUrl: '/agentic-ai-hackathon/', // Your Repo Name with slashes
  organizationName: 'raza-ahmed-khan360', // Your GitHub Username
  projectName: 'agentic-ai-hackathon', // Your Repo Name
  trailingSlash: false, // Required for GitHub Pages to handle links correctly

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Remove this line below if you don't want "Edit this page" links
          editUrl: 'https://github.com/raza-ahmed-khan360/agentic-ai-hackathon/tree/main/',
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/raza-ahmed-khan360/agentic-ai-hackathon/tree/main/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'Agentic AI Book',
      logo: {
        alt: 'AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'The Book',
        },
        // Links to your actual GitHub Repo
        {
          href: 'https://github.com/raza-ahmed-khan360/agentic-ai-hackathon',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Content',
          items: [
            {
              label: 'Read Book',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/raza-ahmed-khan360/agentic-ai-hackathon',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Raza Ahmed Khan. Built with AI.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;