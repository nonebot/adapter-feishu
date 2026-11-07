import { themes } from "prism-react-renderer";

import type { Config } from "@docusaurus/types";
import type { Options as ChangelogOptions } from "@nullbot/docusaurus-plugin-changelog";
import type * as Preset from "@nullbot/docusaurus-preset-nonepress";

// color mode config
const colorMode: Preset.ThemeConfig["colorMode"] = {
  defaultMode: "light",
  respectPrefersColorScheme: true,
};

// navbar config
const navbar: Preset.ThemeConfig["navbar"] = {
  title: "NoneBot",
  logo: {
    alt: "NoneBot",
    src: "logo.png",
    href: "/",
    target: "_self",
    height: 32,
    width: 32,
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
    { label: "更新日志", to: "/changelog/" },
    {
      label: "NoneBot",
      href: "https://github.com/nonebot/nonebot2",
    },
  ],
};

// footer config
const footer: Preset.ThemeConfig["footer"] = {
  style: "light",
  logo: {
    alt: "NoneBot",
    src: "logo.png",
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
const lightCodeTheme = themes.github;
const darkCodeTheme = themes.dracula;

const prism: Preset.ThemeConfig["prism"] = {
  theme: lightCodeTheme,
  darkTheme: darkCodeTheme,
  additionalLanguages: ["docker", "ini"],
};

// algolia config
const algolia: Preset.ThemeConfig["algolia"] = {
  appId: "UJDUZK0SX1",
  apiKey: "0f39628caef1364599979619bc43ede3",
  indexName: "adapter-feishu",
  contextualSearch: true,
};

// nonepress config
const nonepress: Preset.ThemeConfig["nonepress"] = {
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
        href: "https://github.com/nonebot/adapter-feishu",
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
const themeConfig: Preset.ThemeConfig = {
  colorMode,
  navbar,
  footer,
  prism,
  algolia,
  nonepress,
};

export default async function createConfigAsync(): Promise<Config> {
  return {
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

    // Even if you don't use internalization, you can use this field to set
    // useful metadata like html lang. For example, if your site is Chinese, you
    // may want to replace "en" with "zh-Hans".
    i18n: {
      defaultLocale: "zh-Hans",
      locales: ["zh-Hans"],
    },

    presets: [
      [
        "@nullbot/docusaurus-preset-nonepress",
        {
          docs: {
            sidebarPath: require.resolve("./sidebars.ts"),
            // Please change this to your repo.
            editUrl:
              "https://github.com/nonebot/adapter-feishu/edit/master/website/",
            showLastUpdateAuthor: true,
            showLastUpdateTime: true,
          },
          sitemap: {
            changefreq: "daily",
            priority: 0.5,
          },
        } satisfies Preset.Options,
      ],
    ],

    future: {
      faster: true,
      v4: true,
    },

    plugins: [
      require("./src/plugins/webpack-plugin.ts"),
      [
        "@nullbot/docusaurus-plugin-changelog",
        {
          changelogPath: "src/changelog/changelog.md",
          changelogHeader: `description: Changelog
toc_max_heading_level: 2
sidebar_custom_props:
  sidebar_id: changelog
  sidebar_version: current`,
        } satisfies ChangelogOptions,
      ],
    ],

    markdown: {
      mdx1Compat: {
        headingIds: true,
      },
      hooks: {
        onBrokenMarkdownLinks: "warn",
      },
    },

    themeConfig,
  };
}
