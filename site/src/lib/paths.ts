// Every URL lives under the project base path on GitHub Pages.
const base = import.meta.env.BASE_URL.replace(/\/?$/, "/");
export const pageUrl = (path: string): string => base + path.replace(/^\//, "");
export const dataUrl = (name: string): string => `${base}data/${name}`;
