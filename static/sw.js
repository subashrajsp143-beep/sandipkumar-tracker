// Service Worker for M/S Sandip Kumar Material Tracker
const CACHE_NAME = 'sandip-tracker-v2';
const STATIC_ASSETS = [
  '/',
  '/store',
  '/entry',
  '/reports/sites',
  '/reports/daily',
  '/reports/monthly',
  '/attendance',
  '/static/manifest.json',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
  'https://cdn.tailwindcss.com',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css'
];

// Install: Cache critical shell assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Pre-caching static assets');
      return cache.addAll(STATIC_ASSETS).catch(err => console.log('[SW] Pre-cache error:', err));
    })
  );
  self.skipWaiting();
});

// Activate: Clean up old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

// Fetch: Network-First with Cache Fallback for dynamic pages; Cache-First for static images
self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Skip caching non-GET requests (e.g. POST entries handled by client offline queue)
  if (req.method !== 'GET') {
    return;
  }

  // Static images/uploads: Cache First, fallback to network
  if (url.pathname.startsWith('/uploads/') || url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(req).then((cached) => {
        if (cached) return cached;
        return fetch(req).then((res) => {
          if (res && res.status === 200) {
            const copy = res.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
          }
          return res;
        }).catch(() => cached);
      })
    );
    return;
  }

  // HTML Pages & APIs: Network First, fallback to cached version when offline
  event.respondWith(
    fetch(req)
      .then((networkRes) => {
        if (networkRes && networkRes.status === 200) {
          const copy = networkRes.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
        }
        return networkRes;
      })
      .catch(async () => {
        const cached = await caches.match(req);
        if (cached) return cached;
        // Fallback to cached root page if available
        if (req.headers.get('accept') && req.headers.get('accept').includes('text/html')) {
          return caches.match('/');
        }
        return new Response('Offline mode: Internet connection not available', {
          status: 503,
          statusText: 'Offline',
          headers: new Headers({ 'Content-Type': 'text/plain' })
        });
      })
  );
});
