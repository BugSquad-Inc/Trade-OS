import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. frontend/package.json
w("frontend/package.json", """{
  "name": "trade-os-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@tanstack/react-query": "^5.28.4",
    "clsx": "^2.1.0",
    "framer-motion": "^11.0.8",
    "lucide-react": "^0.359.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "tailwind-merge": "^2.2.1",
    "zustand": "^4.5.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.66",
    "@types/react-dom": "^18.2.22",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.18",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.2.2",
    "vite": "^5.1.6"
  }
}
""")

# 2. frontend/vite.config.ts
w("frontend/vite.config.ts", """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
});
""")

# 3. frontend/tsconfig.json
w("frontend/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
""")

# 4. frontend/tsconfig.node.json
w("frontend/tsconfig.node.json", """{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
""")

# 5. frontend/tailwind.config.js
w("frontend/tailwind.config.js", """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', '"SF Mono"', 'ui-monospace', 'Menlo', 'Consolas', 'monospace'],
      },
      colors: {
        apple: {
          blue: '#007AFF',
          green: '#34C759',
          orange: '#FF9500',
          red: '#FF3B30',
          indigo: '#5856D6',
          purple: '#AF52DE',
          teal: '#30B0C7',
          yellow: '#FFCC00',
        }
      },
      borderRadius: {
        '2xl': '16px',
        '3xl': '22px',
        '4xl': '28px',
      }
    },
  },
  plugins: [],
}
""")

# 6. frontend/postcss.config.js
w("frontend/postcss.config.js", """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""")

# 7. frontend/index.html
w("frontend/index.html", """<!doctype html>
<html lang="en" class="dark">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌍</text></svg>" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Trade OS — Export Revenue Operating System</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  </head>
  <body class="bg-zinc-950 text-zinc-100 antialiased selection:bg-blue-500/30 selection:text-blue-200">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
""")

# 8. frontend/src/index.css
w("frontend/src/index.css", """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply font-sans;
  }
}

/* Apple HIG Vibrancy & Glass Materials */
.glass-panel {
  @apply bg-zinc-900/80 backdrop-blur-xl border border-white/[0.08] shadow-2xl;
}

.glass-card {
  @apply bg-zinc-900/60 hover:bg-zinc-850/80 transition-colors backdrop-blur-md border border-white/[0.07] shadow-sm;
}

.glass-inset {
  @apply bg-zinc-950/60 border border-white/[0.05];
}

.glass-topbar {
  @apply bg-zinc-950/80 backdrop-blur-xl border-b border-white/[0.08];
}

.glass-sidebar {
  @apply bg-zinc-950/90 backdrop-blur-2xl border-r border-white/[0.08];
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 9999px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.25);
}
""")

# 9. frontend/src/theme/appleTokens.ts
w("frontend/src/theme/appleTokens.ts", """export const appleTokens = {
  colors: {
    systemBlue: '#007AFF',
    systemGreen: '#34C759',
    systemOrange: '#FF9500',
    systemRed: '#FF3B30',
    systemIndigo: '#5856D6',
    systemPurple: '#AF52DE',
    systemTeal: '#30B0C7',
    systemYellow: '#FFCC00',
  },
  springTransition: {
    type: 'spring',
    stiffness: 400,
    damping: 30,
  },
  gentleSpring: {
    type: 'spring',
    stiffness: 300,
    damping: 25,
  }
};
""")

print("[SUCCESS] Frontend Part 1 (Config, Tailwind, Theme) built successfully")
