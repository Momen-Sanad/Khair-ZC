import type { StorybookConfig } from "@storybook/react-webpack5";

const config: StorybookConfig = {
  stories: ["../src/**/*.mdx", "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"], // Define where to find your story files
  addons: [
    "@storybook/preset-create-react-app", // Preset for Create React App users
    "@storybook/addon-onboarding",        // Storybook onboarding UI
    "@storybook/addon-essentials",        // Essential Storybook addons like actions, controls, docs
    "@chromatic-com/storybook",           // Storybook integration for Chromatic
    "@storybook/addon-interactions",      // Allows interactions testing in Storybook
    "@storybook/addon-a11y",              // Accessibility testing addon
  ],
  framework: {
    name: "@storybook/react-webpack5", // Use Webpack 5 for bundling
    options: {},
  },
  staticDirs: ["../public"], // Static files from the public directory
  webpackFinal: async (config) => {
    // Custom Webpack configurations if needed (e.g., TypeScript support, additional loaders)
    return config;
  },
  typescript: {
    reactDocgen: 'react-docgen', // Configure TypeScript documentation for your components (optional)
  },
};

export default config;
