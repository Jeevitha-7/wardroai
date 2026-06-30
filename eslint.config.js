export default [
  {
    ignores: ["node_modules/**", "frontend/node_modules/**", "frontend/dist/**"],
  },
  {
    files: ["frontend/src/**/*.{js,jsx,ts,tsx}"],
    languageOptions: {
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        ecmaFeatures: { jsx: true },
      },
    },
    rules: {
      "no-unused-vars": "warn",
      "no-undef": "off",
    },
  },
];
