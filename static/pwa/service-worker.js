
const CACHE_NAME = "acz-pwa-v1";
const OFFLINE_PAGE = "/static/pwa/offline.html";

const PRECACHE_FILES = [
  OFFLINE_PAGE,
  "/static/pwa/icon.svg"
];

// Install service worker
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_FILES))
      .then(() => self.skipWaiting())
  );
});

// Activate service worker
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter(
            (name) =>
              name.startsWith("acz-pwa-") &&
              name !== CACHE_NAME
          )
          .map((name) => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

// Handle safe GET requests only
self.addEventListener("fetch", (event) => {
  const request = event.request;

  if (request.method !== "GET") {
    return;
  }

  const url = new URL(request.url);

  if (url.origin !== self.location.origin) {
    return;
  }

  // Never cache private or sensitive pages.
  const privatePaths = [
    "/admin/",
    "/login/",
    "/customer-login/",
    "/customer-register/",
    "/customer-dashboard/",
    "/applications/",
    "/payment-history/",
    "/payment-history-search/",
    "/raise-grievance/",
    "/grievance/"
  ];

  if (
    privatePaths.some((path) =>
      url.pathname.startsWith(path)
    )
  ) {
    return;
  }

  // Cache static assets only.
  if (url.pathname.startsWith("/static/")) {
    event.respondWith(
      caches.open(CACHE_NAME).then(async (cache) => {
        const cached = await cache.match(request);

        if (cached) {
          return cached;
        }

        const response = await fetch(request);

        if (response.ok && response.type === "basic") {
          await cache.put(request, response.clone());
        }

        return response;
      })
    );

    return;
  }

  // Always request pages from the server.
  // Show a generic page if the network is unavailable.
  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request).catch(async () => {
        const offlinePage = await caches.match(OFFLINE_PAGE);

        return offlinePage || new Response(
          "You are offline. Please reconnect to the internet.",
          {
            status: 503,
            headers: {
              "Content-Type": "text/plain; charset=utf-8"
            }
          }
        );
      })
    );
  }
});
