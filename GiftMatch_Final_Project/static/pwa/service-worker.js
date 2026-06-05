const CACHE_NAME = 'giftmatch-cache-v2';
const OFFLINE_URL = '/offline/';
const STATIC_ASSETS = [
  '/',
  OFFLINE_URL,
  '/static/css/styles.css',
  '/static/js/app.js',
  '/static/images/icons/icon-192.png',
  '/static/images/icons/icon-512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.map((key) => key !== CACHE_NAME ? caches.delete(key) : null)))
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request).then((cached) => cached || caches.match(OFFLINE_URL)))
  );
});
