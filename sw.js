const CACHE_NAME = 'ondwari-site-v1';
const CORE_ASSETS = [
  './',
  './index.html',
  './about.html',
  './services.html',
  './works.html',
  './pricing.html',
  './contact.html',
  './insights.html',
  './faq.html',
  './terms.html',
  './privacy.html',
  './project_a.html',
  './article_a.html',
  './404.html',
  './css/loaders/loader.css',
  './css/plugins.css',
  './css/main.css',
  './js/app.js',
  './js/libs.min.js',
  './img/favicon/favicon.ico',
  './img/favicon/icon.svg',
  './img/favicon/manifest.webmanifest'
];

// Install Event: Cache core static shell
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(CORE_ASSETS).catch((err) => {
        console.warn('[ServiceWorker] Core assets caching partial warning:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

// Activate Event: Clean up old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            return caches.delete(cache);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event: Stale-While-Revalidate for static assets, Network-First for navigation
self.addEventListener('fetch', (event) => {
  const { request } = event;

  // Ignore non-GET requests
  if (request.method !== 'GET') return;

  // Handle HTML document navigation (Network first, fallback to Cache)
  if (request.mode === 'navigate' || request.headers.get('accept')?.includes('text/html')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response && response.status === 200) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, responseClone));
          }
          return response;
        })
        .catch(() => {
          return caches.match(request).then((cachedResponse) => {
            if (cachedResponse) return cachedResponse;
            return caches.match('./index.html');
          });
        })
    );
    return;
  }

  // Handle CSS, JS, Fonts, Images (Stale-While-Revalidate)
  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      const fetchPromise = fetch(request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, responseClone));
          }
          return networkResponse;
        })
        .catch(() => {
          // Ignore fetch errors when offline for cached assets
        });

      return cachedResponse || fetchPromise;
    })
  );
});
