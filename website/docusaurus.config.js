// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

// color mode config
/** @type {import('@nullbot/docusaurus-preset-nonepress').ThemeConfig["colorMode"]} */
const colorMode = {
  defaultMode: "light",
  respectPrefersColorScheme: true,
};

// navbar config
/** @type {import('@nullbot/docusaurus-preset-nonepress').ThemeConfig["navbar"]} */
const navbar = {
  title: "NoneBot",
  logo: {
    alt: "",
    src: "logo.png",
    srcDark: "logo.png",
    href: "/",
    target: "_self",
  },
  hideOnScroll: false,
  items: [
    {
      label: "指南",
      type: "docsMenu",
      category: "guide",
    },
    {
      label: "API",
      type: "doc",
      docId: "api/index",
    },
    { label: "更新日志", to: "/changelog" },
    {
      label: "NoneBot",
      icon: ["fas", "angle-double-right"],
      href: "https://github.com/nonebot/nonebot2",
    },
    {
      icon: ["fab", "github"],
      href: "https://github.com/nonebot/adapter-feishu",
    },
  ],
};

// footer config
/** @type {import('@nullbot/docusaurus-preset-nonepress').ThemeConfig["footer"]} */
const footer = {
  style: "light",
  logo: {
    alt: "",
    src: "logo.png",
    srcDark: "logo.png",
    href: "/",
    target: "_self",
    height: 32,
    width: 32,
  },
  copyright: `Copyright © ${new Date().getFullYear()} NoneBot. All rights reserved.`,
  links: [
    {
      title: "Learn",
      items: [
        { label: "Introduction", to: "/docs/guide/" },
        { label: "Installation", to: "/docs/guide/installation" },
      ],
    },
    {
      title: "NoneBot Team",
      items: [{ label: "Homepage", href: "https://nonebot.dev" }],
    },
    {
      title: "Related",
      items: [
        {
          label: "飞书开放平台",
          href: "https://open.feishu.cn/app?lang=zh-CN",
        },
      ],
    },
  ],
};

// prism config
/** @type {import('prism-react-renderer').PrismTheme} */
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line import/order
const lightCodeTheme = require("prism-react-renderer/themes/github");
/** @type {import('prism-react-renderer').PrismTheme} */
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line import/order
const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@nullbot/docusaurus-preset-nonepress').ThemeConfig["prism"]} */
const prism = {
  theme: lightCodeTheme,
  darkTheme: darkCodeTheme,
  additionalLanguages: ["docker", "ini"],
};

// algolia config
/** @type {import('@nullbot/docusaurus-preset-nonepress').ThemeConfig["algolia"]} */
const algolia = {
  appId: "UJDUZK0SX1",
  apiKey: "0f39628caef1364599979619bc43ede3",
  indexName: "adapter-feishu",
  contextualSearch: true,
};

// nonepress config
/** @type {import('@nullbot/docusaurus-preset-nonepress').ThemeConfig["nonepress"]} */
const nonepress = {
  tailwindConfig: require("./tailwind.config"),
  navbar: {
    docsVersionDropdown: {
      dropdownItemsAfter: [
        {
          label: "1.x",
          href: "https://v1.nonebot.dev/",
        },
      ],
    },
    socialLinks: [
      {
        icon: ["fab", "github"],
        href: "https://github.com/nonebot/nonebot2",
      },
    ],
  },
  footer: {
    socialLinks: [
      {
        icon: ["fab", "github"],
        href: "https://github.com/nonebot/nonebot2",
      },
      {
        icon: ["fab", "qq"],
        href: "https://jq.qq.com/?_wv=1027&k=5OFifDh",
      },
      {
        icon: ["fab", "telegram"],
        href: "https://t.me/botuniverse",
      },
      {
        icon: ["fab", "discord"],
        href: "https://discord.gg/VKtE6Gdc4h",
      },
    ],
  },
};

// theme config
/** @type {import('@nullbot/docusaurus-preset-nonepress').ThemeConfig} */
const themeConfig = {
  colorMode,
  navbar,
  footer,
  prism,
  algolia,
  nonepress,
};

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "NoneBot",
  tagline: "飞书协议适配器",
  favicon: "img/favicon.ico",

  // Set the production url of your site here
  url: "https://feishu.adapters.nonebot.dev",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: process.env.BASE_URL || "/",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "nonebot", // Usually your GitHub org/user name.
  projectName: "adapter-feishu", // Usually your repo name.

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "zh-Hans",
    locales: ["zh-Hans"],
  },

  presets: [
    [
      "@nullbot/docusaurus-preset-nonepress",
      /** @type {import('@nullbot/docusaurus-preset-nonepress').Options} */
      ({
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          // Please change this to your repo.
          editUrl:
            "https://github.com/nonebot/adapter-feishu/edit/master/website/",
          showLastUpdateAuthor: true,
          showLastUpdateTime: true,
          // exclude: [
          //   "**/_*.{js,jsx,ts,tsx,md,mdx}",
          //   "**/_*/**",
          //   "**/*.test.{js,jsx,ts,tsx}",
          //   "**/__tests__/**",
          // ],
          // async sidebarItemsGenerator({
          //   isCategoryIndex: defaultCategoryIndexMatcher,
          //   defaultSidebarItemsGenerator,
          //   ...args
          // }) {
          //   return defaultSidebarItemsGenerator({
          //     ...args,
          //     isCategoryIndex(doc) {
          //       // disable category index convention for generated API docs
          //       if (
          //         doc.directories.length > 0 &&
          //         doc.directories.at(-1) === "api"
          //       ) {
          //         return false;
          //       }
          //       return defaultCategoryIndexMatcher(doc);
          //     },
          //   });
          // },
        },
        // theme: {
        //   customCss: require.resolve("./src/css/custom.css"),
        // },
        sitemap: {
          changefreq: "daily",
          priority: 0.5,
        },
      }),
    ],
  ],
  plugins: [require("./src/plugins/webpack-plugin.cjs")],

  themeConfig,
};

module.exports = config;
