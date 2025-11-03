
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error("Could not find root element to mount to");
}

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Gemini AI Multi-Modal Studio</title>
    <script src="https://cdn.tailwindcss.com"></script>
  <script type="importmap">
{
  "imports": {
    "react/": "https://aistudiocdn.com/react@^19.2.0/",
    "react": "https://aistudiocdn.com/react@^19.2.0",
    "react-dom/": "https://aistudiocdn.com/react-dom@^19.2.0/",
    "@heroicons/react/": "https://aistudiocdn.com/@heroicons/react@^2.2.0/",
    "@google/genai": "https://aistudiocdn.com/@google/genai@^1.27.0",
    "@vitejs/plugin-react": "https://aistudiocdn.com/@vitejs/plugin-react@^5.1.0",
    "path": "https://aistudiocdn.com/path@^0.12.7",
    "vite": "https://aistudiocdn.com/vite@^7.1.12",
    "@testing-library/jest-dom": "https://aistudiocdn.com/@testing-library/jest-dom@^6.9.1",
    "@testing-library/react": "https://aistudiocdn.com/@testing-library/react@^16.3.0",
    "@testing-library/user-event": "https://aistudiocdn.com/@testing-library/user-event@^14.6.1",
    "vitest": "https://aistudiocdn.com/vitest@^4.0.6",
    "vitest/": "https://aistudiocdn.com/vitest@^4.0.6/"
  }
}
</script>
<link rel="stylesheet" href="/index.css">
</head>
  <body class="bg-gray-900 text-white">
    <div id="root"></div>
    <script type="module" src="/index.tsx"></script>
  </body>
</html><!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Gemini AI Multi-Modal Studio</title>
    <script src="https://cdn.tailwindcss.com"></script>
  <script type="importmap">
{
  "imports": {
    "react/": "https://aistudiocdn.com/react@^19.2.0/",
    "react": "https://aistudiocdn.com/react@^19.2.0",
    "react-dom/": "https://aistudiocdn.com/react-dom@^19.2.0/",
    "@heroicons/react/": "https://aistudiocdn.com/@heroicons/react@^2.2.0/",
    "@google/genai": "https://aistudiocdn.com/@google/genai@^1.27.0",
    "@vitejs/plugin-react": "https://aistudiocdn.com/@vitejs/plugin-react@^5.1.0",
    "path": "https://aistudiocdn.com/path@^0.12.7",
    "vite": "https://aistudiocdn.com/vite@^7.1.12"
  }
}
</script>
<link rel="stylesheet" href="/index.css">
</head>
  <body class="bg-gray-900 text-white">
    <div id="root"></div>
    <script type="module" src="/index.tsx"></script>
  </body>
</html>{
  "name": "gemini-ai-multi-modal-studio",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^19.2.0",
    "react-dom": "^19.2.0",
    "@heroicons/react": "^2.2.0",
    "@google/genai": "^1.27.0"
  },
  "devDependencies": {
    "@types/node": "^22.14.0",
    "@vitejs/plugin-react": "^5.0.0",
    "typescript": "~5.8.2",
    "vite": "^6.2.0"
  }
}
<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/drive/1Y-jFui4UZHK5FW7DE8885dLTtz-Xw5Xf

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`

https://ai.studio/apps/drive/1IS4g00UO3Uy8g7zdEoVR3iTlshZ1B3fX
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Gemini AI Multi-Modal Studio</title>
    <script src="https://cdn.tailwindcss.com"></script>
  <script type="importmap">
{
  "imports": {
    "react/": "https://aistudiocdn.com/react@^19.2.0/",
    "react": "https://aistudiocdn.com/react@^19.2.0",
    "react-dom/": "https://aistudiocdn.com/react-dom@^19.2.0/",
    "@heroicons/react/": "https://aistudiocdn.com/@heroicons/react@^2.2.0/",
    "@google/genai": "https://aistudiocdn.com/@google/genai@^1.27.0",
    "@vitejs/plugin-react": "https://aistudiocdn.com/@vitejs/plugin-react@^5.1.0",
    "path": "https://aistudiocdn.com/path@^0.12.7",
    "vite": "https://aistudiocdn.com/vite@^7.1.12",
    "@testing-library/jest-dom": "https://aistudiocdn.com/@testing-library/jest-dom@^6.9.1",
    "@testing-library/react": "https://aistudiocdn.com/@testing-library/react@^16.3.0",
    "@testing-library/user-event": "https://aistudiocdn.com/@testing-library/user-event@^14.6.1",
    "vitest": "https://aistudiocdn.com/vitest@^4.0.6",
    "vitest/": "https://aistudiocdn.com/vitest@^4.0.6/"
  }
}
</script>
<link rel="stylesheet" href="/index.css">
</head>
  <body class="bg-gray-900 text-white">
    <div id="root"></div>
    <script type="module" src="/index.tsx"></script>
  </body>
</html>
