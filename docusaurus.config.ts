import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  clientModules: ['./src/clientModules/imageZoom.js'],
  title: 'MZpack',
  tagline: 'Order flow analysis and algorithmic trading for NinjaTrader 8',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://docs.mzpack.pro',
  baseUrl: '/',

  organizationName: 'mikhail-zhelnov',
  projectName: 'mzpack-docs',
  trailingSlash: false,

  onBrokenLinks: 'throw',

  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

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
          editUrl: 'https://github.com/mikhail-zhelnov/mzpack-docs/edit/main/',
        },
        blog: {
          showReadingTime: true,
          blogTitle: 'Release Notes',
          blogDescription: 'MZpack release notes and changelog',
          editUrl: 'https://github.com/mikhail-zhelnov/mzpack-docs/edit/main/',
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'api',
        path: 'api',
        routeBasePath: 'api',
        sidebarPath: './sidebarsApi.ts',
        editUrl: 'https://github.com/mikhail-zhelnov/mzpack-docs/edit/main/',
      },
    ],
  ],

  themes: [
    [
      '@easyops-cn/docusaurus-search-local',
      {
        hashed: true,
        docsRouteBasePath: ['docs', 'api'],
        docsDir: ['docs', 'api'],
        indexBlog: false,
      },
    ],
  ],

  themeConfig: {
    image: 'img/mzpack-social-card.png',
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'MZpack',
      logo: {
        alt: 'MZpack Logo',
        src: 'img/logo.svg',
        srcDark: 'img/logo-dark.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'userGuideSidebar',
          position: 'left',
          label: 'User Guide',
        },
        {
          to: '/api/getting-started/overview',
          label: 'API Reference',
          position: 'left',
          activeBaseRegex: '/api/',
        },
        {to: '/blog', label: 'Release Notes', position: 'left'},
        {
          href: 'https://github.com/mikhail-zhelnov/mzpack-docs',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'User Guide',
              to: '/docs/getting-started/installation',
            },
            {
              label: 'API Reference',
              to: '/api/getting-started/overview',
            },
            {
              label: 'FAQ',
              to: '/docs/faq',
            },
          ],
        },
        {
          title: 'Product',
          items: [
            {
              label: 'MZpack.pro',
              href: 'https://mzpack.pro',
            },
            {
              label: 'NinjaTrader',
              href: 'https://ninjatrader.com',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Release Notes',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/mikhail-zhelnov/mzpack-docs',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} MZpack. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['csharp'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
